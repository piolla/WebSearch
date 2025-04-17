import os 
import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="웹 검색 챗봇", page_icon="🤖")
st.title("🔍 웹 검색 가능한 AI 챗봇")

# 사이드바에 API 키 입력 받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API 키", type="password")
    st.markdown("---")
    st.markdown("**참고:** GPT-4o-search-preview 모델과 웹 검색 기능을 사용합니다.")

# 세션 상태에 메시지 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("궁금한 것을 물어보세요!"):
    # API 키 확인
    #if not openai_api_key:
    #    st.info("사이드바에서 OpenAI API 키를 입력해주세요.")
    #    st.stop()
    
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답 생성
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            completion = client.chat.completions.create(
                model="gpt-4o-search-preview",
                web_search_options={},
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"⚠️ 오류 발생: {str(e)}"
        
        response_placeholder.markdown(response)

    # 어시스턴트 응답 기록 저장
    st.session_state.messages.append({"role": "assistant", "content": response})