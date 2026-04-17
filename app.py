import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ================= 1. 초정밀 명리 지식 베이스 (DB) =================

# 10천간(일간) 고유 성향
KAN_DESC = {
    "갑": "위로 뻗어가는 거목 - 강한 추진력과 리더십",
    "을": "유연한 담쟁이 - 적응력과 질긴 생명력",
    "병": "하늘의 태양 - 열정적이고 화려한 자기표현",
    "정": "따뜻한 등불 - 섬세하고 헌신적인 내면의 빛",
    "무": "넓은 대지 - 포용력과 묵직한 신뢰감",
    "기": "비옥한 전답 - 안정적이고 실속 있는 관리 능력",
    "경": "단단한 바위 - 강직한 결단력과 원칙주의",
    "신": "정교한 보석 - 예리한 분석력과 완벽주의",
    "임": "거대한 강물 - 깊은 지혜와 유연한 전략",
    "계": "만물을 적시는 비 - 세심한 통찰력과 창의성"
}

# 십성(Ten Gods) 사회적 기능
TEN_GODS = {
    "비겁": {"title": "주관과 독립", "desc": "자기 주도적인 학습과 경쟁 속에서 성장합니다."},
    "식상": {"title": "창의와 표현", "desc": "아이디어를 표출하고 응용하는 데 천재성을 보입니다."},
    "재성": {"title": "결과와 관리", "desc": "목표가 명확할 때 최고의 효율을 발휘합니다."},
    "관성": {"title": "명예와 규율", "desc": "원칙을 준수하고 체계적인 환경에서 안정감을 느낍니다."},
    "인성": {"title": "수용과 사색", "desc": "지식을 습득하고 깊이 고민하는 탐구심이 강합니다."}
}

# ================= 2. 명리 분석 엔진 (Core Logic) =================

class ProSajuEngine:
    def __init__(self, name, birth_data, il_gan):
        self.name = name
        self.il_gan = il_gan
        self.elements = self._calculate_complex_elements(birth_data)
        self.strength = self._analyze_energy_strength()
        self.lucky_elements = self._get_lucky_items()

    def _calculate_complex_elements(self, data):
        # 생년월일시 해시값을 이용한 정밀 오행 분배 (가상 시뮬레이션 로직)
        hash_val = data.year + data.month + data.day
        scores = {
            "목": (hash_val * 7) % 35 + 5,
            "화": (hash_val * 13) % 35 + 5,
            "토": (hash_val * 19) % 35 + 5,
            "금": (hash_val * 23) % 35 + 5,
            "수": (hash_val * 29) % 35 + 5
        }
        return scores

    def _analyze_energy_strength(self):
        # 일간과 타 오행의 상생상극 수치화 (신강/신약 판별)
        my_power = self.elements[self.il_gan]
        # 단순 점수화가 아닌 상대적 비중으로 계산
        total = sum(self.elements.values())
        ratio = (my_power / total) * 100
        return int(ratio - 20) # 기준점 대비 수치

    def _get_lucky_items(self):
        weakest = min(self.elements, key=self.elements.get)
        lucky_map = {
            "목": {"color": "Green", "num": "3, 8", "food": "신선한 채소"},
            "화": {"color": "Red", "num": "2, 7", "food": "쓴맛의 차"},
            "토": {"color": "Yellow", "num": "5, 10", "food": "단호박"},
            "금": {"color": "White", "num": "4, 9", "food": "매운 음식"},
            "수": {"color": "Blue", "num": "1, 6", "food": "짠맛의 해조류"}
        }
        return lucky_map[weakest]

# ================= 3. UI 및 리포트 구성 (Frontend) =================

def main():
    st.set_page_config(page_title="프리미엄 사주 컨설팅", layout="wide")
    
    # 현대적인 스타일링
    st.markdown("""
        <style>
        .report-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #eee; }
        .highlight { color: #2C3E50; font-weight: bold; border-left: 5px solid #2C3E50; padding-left: 10px; margin: 15px 0; }
        .lucky-item { display: inline-block; padding: 8px 15px; background: #f1f2f6; border-radius: 10px; margin-right: 10px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛡️ AI 사주 기반 정밀 학습/운세 리포트")

    with st.sidebar:
        st.header("📋 정보 입력")
        name = st.text_input("학생/사용자 이름", "김준우")
        b_date = st.date_input("생년월일", value=datetime(1983, 11, 8))
        b_time = st.time_input("출생시간")
        il_gan = st.selectbox("본인의 일간(본질)", list(KAN_DESC.keys()))
        st.divider()
        submit = st.button("전문 리포트 생성")

    if submit:
        # 엔진 구동
        engine = ProSajuEngine(name, b_date, il_gan)
        strong_elem = max(engine.elements, key=engine.elements.get)
        
        # 레이아웃 배치
        col1, col2 = st.columns([1, 1.2])

        with col1:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.subheader("📊 오행 에너지 밸런스")
            # 레이더 차트
            fig = go.Figure(data=go.Scatterpolar(
                r=list(engine.elements.values()), theta=list(engine.elements.keys()),
                fill='toself', line_color='#2C3E50'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            st.write(f"**에너지 상태:** {'신강(강한 자아)' if engine.strength > 5 else '신약(유연한 자아)' if engine.strength < -5 else '중화(균형 잡힌 자아)'}")
            st.progress(max(0, min((engine.strength + 30) / 60, 1.0)))
            st.markdown('</div>', unsafe_allow_html=True)

            # 섹션: 행운의 요소
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.subheader("🍀 오늘의 행운 처방")
            st.write(f"🎨 **색상:** {engine.lucky_elements['color']}")
            st.write(f"🔢 **숫자:** {engine.lucky_elements['num']}")
            st.write(f"🥗 **음식:** {engine.lucky_elements['food']}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.subheader(f"📜 {name}님만을 위한 심층 분석")
            
            # 1. 기질 분석
            st.markdown(f'<div class="highlight">본질적 성향: {KAN_DESC[il_gan]}</div>', unsafe_allow_html=True)
            st.write(f"{name}님은 {il_gan}의 본질을 가지고 있으나, 현재 사주 내에 {strong_elem}의 기운이 {engine.elements[strong_elem]}%로 매우 강하게 작용하고 있습니다.")
            
            # 2. 십성 학습 전략 (동적 생성)
            # 여기서는 '식상'이 강한 경우로 예시 로직 구성
            st.markdown('<div class="highlight">학습 및 사회적 전략</div>', unsafe_allow_html=True)
            st.info(f"**현재 격국:** 식상(창의형) 발달\n\n{name}님은 단순 암기보다 원리를 이해하고 표출할 때 시너지가 납니다. '설명하는 공부법'이 성적 향상의 핵심입니다.")
            
            # 3. 월간 운세 리포트
            st.markdown('<div class="highlight">이달의 흐름과 소견</div>', unsafe_allow_html=True)
            st.warning("이번 달은 주변과의 소통에서 에너지가 많이 소모될 수 있습니다. 중요한 결정은 '금'의 기운이 강한 오후 시간에 내리는 것이 유리합니다.")
            
            st.divider()
            st.subheader("👨‍🏫 전문가 총평")
            st.write(f"\"{name}님은 맑은 지혜를 품은 사주입니다. 넘치는 아이디어를 현실적인 결과로 바꾸기 위해선 '계획의 시각화'가 반드시 동반되어야 합니다. 행운의 숫자를 활용해 공부 시간을 정해보세요!\"")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
