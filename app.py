import streamlit as st
import openai
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT 호출 함수
def ask_gpt(prompt, model="gpt-4", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

# STP 분석
def generate_stp_analysis(company_desc):
    prompt = f"""
당신은 마케팅 분석가입니다. 아래는 한 회사의 상황 설명입니다.

"{company_desc}"

이 회사에 대해 STP(Segmentation, Targeting, Positioning) 분석을 해주세요.
각 항목을 명확하게 구분해서 설명해주세요.
"""
    return ask_gpt(prompt)

# 4P 전략 도출
def generate_4p_plan(stp_analysis):
    prompt = f"""
당신은 마케팅 전략 전문가입니다.
아래는 STP 분석 결과입니다:

{stp_analysis}

이 분석을 기반으로 4P 전략(Product, Price, Place, Promotion)을 구체적으로 작성해주세요.
"""
    return ask_gpt(prompt)

# 유통 채널 추천
def recommend_distribution_channel(four_p_analysis):
    prompt = f"""
다음은 한 회사의 4P 마케팅 전략입니다:

{four_p_analysis}

이 전략을 바탕으로 가장 적합한 유통 채널을 하나 추천하고, 이유를 설명해주세요.
(예: 자사몰, 쿠팡, 네이버 스마트스토어, 백화점, 드럭스토어, 대리점 등)
"""
    return ask_gpt(prompt)


# Streamlit UI
st.set_page_config(page_title="STP/4P 마케팅 분석기", layout="wide")

st.title("📊 ChatGPT 기반 마케팅 분석기 (STP → 4P → 유통 채널 추천)")

company_input = st.text_area("💬 회사의 현재 상황을 입력하세요", height=200, placeholder="예: 2030 여성 대상 친환경 화장품을 자사몰 위주로 소량 판매 중이나 최근 매출 감소...")

if st.button("🔍 분석 시작"):
    if company_input.strip() == "":
        st.warning("회사 상황을 먼저 입력하세요.")
    else:
        with st.spinner("STP 분석 중..."):
            stp_result = generate_stp_analysis(company_input)
            st.subheader("🧩 STP 분석 결과")
            st.markdown(stp_result)

        with st.spinner("4P 전략 도출 중..."):
            four_p_result = generate_4p_plan(stp_result)
            st.subheader("📦 4P 전략 결과")
            st.markdown(four_p_result)

        with st.spinner("유통 채널 추천 중..."):
            channel_result = recommend_distribution_channel(four_p_result)
            st.subheader("🚚 추천 유통 채널")
            st.markdown(channel_result)
