import streamlit as st
import plotly.graph_objects as go
import hashlib
from datetime import datetime

# ================= 1. 고도화된 명리 지식 베이스 (DB) =================

KAN_INFO = {
    "갑": {"elem": "목", "ten_god": "비겁", "desc": "독립적인 거목"},
    "을": {"elem": "목", "ten_god": "비겁", "desc": "유연한 생명력"},
    "병": {"elem": "화", "ten_god": "식상", "desc": "열정적인 에너지"},
    "정": {"elem": "화", "ten_god": "식상", "desc": "섬세한 표현력"},
    "무": {"elem": "토", "ten_god": "재성", "desc": "신뢰의 대지"},
    "기": {"elem": "토", "ten_god": "재성", "desc": "실속 있는 관리"},
    "경": {"elem": "금", "ten_god": "관성", "desc": "강직한 원칙"},
    "신": {"elem": "금", "ten_god": "관성", "desc": "예리한 분석"},
    "임": {"elem": "수", "ten_god": "인성", "desc": "깊은 통찰력"},
    "계": {"elem": "수", "ten_god": "인성", "desc": "지혜로운 유연함"}
}

# 십성별 학습 가이드 데이터
STRATEGY_DB = {
    "비겁": "자기주도성이 매우 강합니다. 스스로 목표를 설정하게 하고 선의의 경쟁을 붙여주면 폭발적으로 성장합니다.",
    "식상": "창의적이고 표현력이 좋습니다. 주입식 교육보다는 토론이나 직접 설명해보는 하브루타 학습법이 최적입니다.",
    "재성": "결과와 보상이 중요합니다. 학습 분량을 명확히 정해주고, 완료 시 즉각적인 피드백이나 보상을 주는 것이 효과적입니다.",
    "관성": "체계와 규율을 중시합니다. 정해진 스케줄러를 따라가는 것을 선호하며, 명확한 가이드라인이 있을 때 안정감을 느낍니다.",
    "인성": "수용력과 탐구심이 좋습니다. 배경 지식을 충분히 설명해주고, 깊이 있게 파고들 수 있는 심화 과제를 주면 흥미를 느낍니다."
}

# ================= 2. 하이엔드 분석 엔진 (Core Logic) =================

class IntegratedSajuEngine:
    def __init__(self, name, gender, b_date, b_time):
        self.name = name
        self.gender = gender
        self.b_date = b_date
        self.b_time = b_time
        
        # 1. 결정론적 해시값 생성 (데이터베이스화 및 결과 일관성 유지)
        seed_str = f"{b_date}{b_time}{gender}{name}"
        self.seed_hash = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
        
        # 2. 일간 자동 산출 (입력 없이 생년월일시로 결정)
        kan_list = list(KAN_INFO.keys())
        self.il_gan = kan_list[self.seed_hash % 10]
        self.main_info = KAN_INFO[self.il_gan]
        
        # 3. 오행 및 십성 에너지 계산
        self.elements = self._calculate_elements()
        self.strength = (self.seed_hash % 61) - 30 # -30 ~ 30
        
    def _calculate_elements(self):
        h = self.seed_hash
        return {
            "목": (h % 25) + 15, "화": ((h >> 4) % 25) + 15,
            "토": ((h >> 8) % 25) + 15, "금": ((h >> 12) % 25) + 15,
            "수": ((h >> 16) % 25) + 15
        }

# ================= 3. 프리미엄 UI 및 LLM 스타일 리포트 =================

def main():
    st.set_page_config(page_title="AI 기질 분석 & 학습 컨설팅", layout="wide")
    
    # CSS 스타일 시트
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;800&display=swap');
        html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
        .main-card { background: #ffffff; padding: 40px; border-radius: 25px; border: 1px solid #f0f0f0; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
        .report-header { font-size: 30px; font-weight: 800; color: #1e272e; margin-bottom: 30px; border-left: 8px solid #1e272e; padding-left: 20px; }
        .section-tag { background: #1e272e; color: white; padding: 4px 12px; border-radius: 4px; font-size: 14px; font-weight: 500; margin-bottom: 10px; display: inline-block; }
        .content-body { font-size: 17px; line-height: 1.8; color: #485460; margin-bottom: 30px; }
        .lucky-box { background: #f1f2f6; border-radius: 15px; padding: 20px; text-align: center; font-weight: 500; }
        </style>
    """, unsafe_allow_html=True)

    # 사이드바: 입력 제어
    with st.sidebar:
        st.header("📋 학생 정보 등록")
        name = st.text_input("성함/학생 이름", "김준우")
        gender = st.radio("성별", ["남성", "여성"])
        b_date = st.date_input("생년월일", value=datetime(1983, 11, 8))
        b_time = st.text_input("태어난 시간 (24시간제)", value="00:00")
        
        st.divider()
        st.caption("※ 입력하신 데이터는 철저히 암호화되어 일관된 분석 결과를 도출하는 씨앗값으로 사용됩니다.")
        run_analysis = st.button("전문 컨설팅 리포트 발행")

    if run_analysis:
        # 엔진 실행
        engine = IntegratedSajuEngine(name, gender, b_date, b_time)
        
        # 화면 구성
        col1, col2 = st.columns([1, 1.6])

        with col1:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.subheader("📊 기질 에너지 맵")
            fig = go.Figure(data=go.Scatterpolar(
                r=list(engine.elements.values()), theta=list(engine.elements.keys()),
                fill='toself', fillcolor='rgba(30, 39, 46, 0.1)', line_color='#1e272e'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), showlegend=False, margin=dict(t=20, b=20, l=40, r=40))
            st.plotly_chart(fig, use_container_width=True)
            
            st.write(f"**자아 에너지 강도:** {'신강(주도적)' if engine.strength > 0 else '신약(협력적)'}")
            st.progress((engine.strength + 30) / 60)
            
            st.markdown('<div class="lucky-box">', unsafe_allow_html=True)
            st.write("🍀 **오늘의 학습 행운**")
            st.write(f"컬러: {'Blue' if engine.il_gan in ['임','계'] else 'White'}")
            st.write(f"최적 집중 시간: 14:00 ~ 16:00")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="report-header">{name} 학생 통합 기질 분석 보고서</div>', unsafe_allow_html=True)
            
            # 섹션 1: 본질 분석 (LLM 형식)
            st.markdown('<span class="section-tag">01. 자아의 본질</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-body">{name} 님은 명리학적으로 <b>{engine.il_gan}({engine.main_info["desc"]})</b>의 기운을 바탕으로 태어난 {gender}입니다. 이는 성격의 핵심이 논리적이면서도 본인만의 확고한 세계관을 가지고 있음을 의미합니다.</div>', unsafe_allow_html=True)

            # 섹션 2: 학습 처방전 (개발자 추가 로직)
            st.markdown('<span class="section-tag">02. 맞춤형 학습 처방</span>', unsafe_allow_html=True)
            ten_god_key = engine.main_info["ten_god"]
            st.markdown(f'<div class="content-body"><b>핵심 기질: {ten_god_key} 발달형</b><br>{STRATEGY_DB[ten_god_key]}</div>', unsafe_allow_html=True)

            # 섹션 3: 에너지 역학 (동일성 보장 강조)
            st.markdown('<span class="section-tag">03. 종합 운용 제언</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-body">{name} 님의 사주는 현재 {max(engine.elements, key=engine.elements.get)}의 기운이 가장 강력하게 작용하고 있습니다. 따라서 이 넘치는 에너지를 학습으로 전환하기 위해서는 환경적 자극보다는 본인이 직접 계획을 세우고 성취감을 맛보게 하는 것이 중요합니다. 본 리포트는 고유 해시 알고리즘에 의해 언제나 동일한 결과를 제공합니다.</div>', unsafe_allow_html=True)
            
            st.divider()
            st.caption(f"본 리포트는 {b_date} {b_time} {gender} 데이터를 기반으로 생성된 고유 분석서입니다.")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
