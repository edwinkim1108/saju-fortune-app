import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. 천간 데이터 및 오행 매핑
KAN_INFO = {
    "갑": {"elem": "목", "desc": "위로 뻗어가는 거목 - 강한 추진력과 리더십"},
    "을": {"elem": "목", "desc": "유연한 담쟁이 - 적응력과 질긴 생명력"},
    "병": {"elem": "화", "desc": "하늘의 태양 - 열정적이고 화려한 자기표현"},
    "정": {"elem": "화", "desc": "따뜻한 등불 - 섬세하고 헌신적인 내면의 빛"},
    "무": {"elem": "토", "desc": "넓은 대지 - 포용력과 묵직한 신뢰감"},
    "기": {"elem": "토", "desc": "비옥한 전답 - 안정적이고 실속 있는 관리 능력"},
    "경": {"elem": "금", "desc": "단단한 바위 - 강직한 결단력과 원칙주의"},
    "신": {"elem": "금", "desc": "정교한 보석 - 예리한 분석력과 완벽주의"},
    "임": {"elem": "수", "desc": "거대한 강물 - 깊은 지혜와 유연한 전략"},
    "계": {"elem": "수", "desc": "만물을 적시는 비 - 세심한 통찰력과 창의성"}
}

class ProSajuEngine:
    def __init__(self, name, birth_data, il_gan):
        self.name = name
        self.il_gan = il_gan
        self.il_gan_elem = KAN_INFO[il_gan]["elem"] # 천간을 오행으로 변환
        self.elements = self._calculate_complex_elements(birth_data)
        self.strength = self._analyze_energy_strength()
        self.lucky_elements = self._get_lucky_items()

    def _calculate_complex_elements(self, data):
        # 고유 해시 로직 (생년월일시에 따른 가변성 확보)
        val = data.year + data.month + data.day
        scores = {
            "목": (val * 7) % 35 + 10,
            "화": (val * 13) % 35 + 10,
            "토": (val * 19) % 35 + 10,
            "금": (val * 23) % 35 + 10,
            "수": (val * 29) % 35 + 10
        }
        return scores

    def _analyze_energy_strength(self):
        # 에러 해결 포인트: self.il_gan_elem 사용
        my_power = self.elements[self.il_gan_elem]
        total = sum(self.elements.values())
        return int((my_power / total * 100) - 20)

    def _get_lucky_items(self):
        weakest = min(self.elements, key=self.elements.get)
        lucky_map = {
            "목": {"color": "Green", "num": "3, 8", "food": "채소"},
            "화": {"color": "Red", "num": "2, 7", "food": "차"},
            "토": {"color": "Yellow", "num": "5, 10", "food": "단호박"},
            "금": {"color": "White", "num": "4, 9", "food": "견과류"},
            "수": {"color": "Blue", "num": "1, 6", "food": "해조류"}
        }
        return lucky_map[weakest]

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="고정밀 명리 분석 Pro", layout="wide")
    
    with st.sidebar:
        st.header("📋 정보 입력")
        name = st.text_input("이름", "김준우")
        b_date = st.date_input("생년월일", value=datetime(1983, 11, 8))
        il_gan = st.selectbox("본인의 일간(천간)", list(KAN_INFO.keys()))
        submit = st.button("전문 리포트 생성")

    if submit:
        engine = ProSajuEngine(name, b_date, il_gan)
        
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.subheader("📊 에너지 분포")
            fig = go.Figure(data=go.Scatterpolar(r=list(engine.elements.values()), theta=list(engine.elements.keys()), fill='toself'))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.header(f"📜 {name}님의 정밀 리포트")
            st.info(f"**본질적 성향:** {KAN_INFO[il_gan]['desc']}")
            st.success(f"**에너지 상태:** {'신강' if engine.strength > 0 else '신약'} (지수: {engine.strength})")
            
            st.divider()
            st.write("### 🍀 오늘의 행운 처방")
            st.write(f"🎨 컬러: {engine.lucky_elements['color']} | 🔢 숫자: {engine.lucky_elements['num']}")

if __name__ == "__main__":
    main()
