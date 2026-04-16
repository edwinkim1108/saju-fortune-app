import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ================= 1. 데이터베이스 및 알고리즘 =================
# 점신 스타일의 상세 해설 DB
FORTUNE_DB = {
    "오늘의행운": {
        "색상": ["#FFFFFF (순수와 시작)", "#2C3E50 (신뢰와 안정)", "#E74C3C (열정과 에너지)", "#F1C40F (희망과 풍요)"],
        "숫자": ["1", "3", "7", "8"],
        "음식": ["따뜻한 차", "견과류", "신선한 샐러드", "매콤한 요리"],
        "방향": ["동쪽 (새로운 기운)", "남쪽 (활기찬 기운)", "북쪽 (차분한 기운)"]
    },
    "월간운세": {
        "총평": "이번 달은 수(水)의 기운이 강해지는 시기로, 급한 결정보다는 내실을 다지는 것이 좋습니다.",
        "주의": "대인관계에서 오해가 생길 수 있으니 경청하는 자세가 필요합니다."
    }
}

ELEMENT_STYLES = {
    "목": {"color": "#2ECC71", "label": "창의와 시작"},
    "화": {"color": "#E74C3C", "label": "열정과 표현"},
    "토": {"color": "#F1C40F", "label": "안정과 신뢰"},
    "금": {"color": "#95A5A6", "label": "결단과 원칙"},
    "수": {"color": "#3498DB", "label": "지혜와 유연"}
}

# ================= 2. 시각화 컴포넌트 =================
class JeomsinVisualizer:
    @staticmethod
    def draw_radar(elements):
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(elements.values()),
            theta=list(elements.keys()),
            fill='toself',
            fillcolor='rgba(52, 152, 219, 0.2)',
            line=dict(color='#3498DB', width=2)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 60])),
            showlegend=False, height=300, margin=dict(t=20, b=20, l=40, r=40)
        )
        return fig

# ================= 3. 메인 어플리케이션 UI =================
def main():
    st.set_page_config(page_title="점신 스타일 통합 사주", layout="wide")

    # 고퀄리티 CSS 커스텀
    st.markdown("""
        <style>
        .main { background-color: #F8F9FA; }
        .card {
            background-color: white; padding: 25px; border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        }
        .lucky-item {
            display: inline-block; padding: 8px 15px; border-radius: 10px;
            background-color: #F1F2F6; margin-right: 10px; font-weight: bold;
        }
        .section-title { font-size: 22px; font-weight: bold; color: #2C3E50; margin-bottom: 15px; }
        </style>
    """, unsafe_allow_html=True)

    # 헤더 섹션
    st.title("🔮 통합 명리 컨설팅 리포트 (Pro)")
    st.write(f"오늘의 날짜: {datetime.now().strftime('%Y년 %m월 %d일')}")

    with st.sidebar:
        st.header("👤 사용자 정보")
        name = st.text_input("성함", "김준우")
        gender = st.radio("성별", ["남성", "여성"])
        birth_date = st.date_input("생년월일")
        birth_time = st.time_input("출생시간")
        il_gan = st.selectbox("일간(본질) 선택", ["금", "수", "목", "화", "토"])
        st.divider()
        st.button("운세 새로고침")

    # 가상 데이터 (점신 분석 결과 재현)
    mock_elements = {"목": 10, "화": 15, "토": 10, "금": 12, "수": 53}
    
    # 레이아웃 배치
    col1, col2 = st.columns([1, 1.3])

    with col1:
        # 섹션 1: 오늘의 행운
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🍀 오늘의 행운 처방</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        cols[0].write(f"🎨 **행운의 색:** \n{FORTUNE_DB['오늘의행운']['색상'][2]}")
        cols[1].write(f"🔢 **행운의 숫자:** \n{FORTUNE_DB['오늘의행운']['숫자'][2]}")
        cols[0].write(f"🍲 **행운의 음식:** \n{FORTUNE_DB['오늘의행운']['음식'][0]}")
        cols[1].write(f"🧭 **행운의 방향:** \n{FORTUNE_DB['오늘의행운']['방향'][0]}")
        st.markdown('</div>', unsafe_allow_html=True)

        # 섹션 2: 오행 밸런스
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 오행 에너지 분석</div>', unsafe_allow_html=True)
        st.plotly_chart(JeomsinVisualizer.draw_radar(mock_elements), use_container_width=True)
        st.write(f"현재 **수(水)** 기운이 매우 강합니다. 이는 지혜를 뜻하지만, 동시에 생각이 많아질 수 있음을 의미합니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # 섹션 3: 종합 사주 풀이
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">📜 {name}님의 종합 사주 리포트</div>', unsafe_allow_html=True)
        st.write(f"**[{il_gan}]**의 기운을 타고난 당신은 정교한 분석력과 논리적인 사고를 가졌습니다.")
        
        tab1, tab2, tab3 = st.tabs(["💡 성향/학습", "💰 재물/명예", "📅 월간 흐름"])
        
        with tab1:
            st.info(f"**[식신/상관 발달형]**\n\n두뇌 회전이 매우 빠릅니다. {name}님은 단순 반복보다는 원리를 파악하고 이를 응용하는 데 탁월한 능력을 보입니다. 공부나 업무 시 '왜?'라는 질문에 답을 찾아가는 과정이 반드시 필요합니다.")
        with tab2:
            st.success("**[재물운/사회운]**\n\n현재 운의 흐름상 전문 기술이나 자격증을 활용한 재물 취득이 유리합니다. 조직 내에서는 기획이나 전략 파트에서 빛을 발할 사주입니다.")
        with tab3:
            st.warning(f"**[2026년 {datetime.now().month}월 운세]**\n\n{FORTUNE_DB['월간운세']['총평']}\n\n* **특히 주의할 날:** 7일, 19일 (감정적인 지출 주의)")
        st.markdown('</div>', unsafe_allow_html=True)

        # 섹션 4: 전문가 제안 (점신 스타일)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">👨‍🏫 전문가 총평</div>', unsafe_allow_html=True)
        st.write(f"\"{name}님은 맑은 물속에 담긴 날카로운 칼과 같습니다. 영리함은 갖췄으나 스스로를 너무 검열하는 경향이 있습니다. 가끔은 '그냥 하는' 무심함이 성취를 앞당길 것입니다.\"")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
