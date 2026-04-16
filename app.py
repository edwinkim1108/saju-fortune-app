import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ================= 1. 고급 명리 데이터 시스템 =================
ELEMENT_INFO = {
    "목": {"color": "#2ECC71", "desc": "추진력과 성장"},
    "화": {"color": "#E74C3C", "desc": "열정과 표현력"},
    "토": {"color": "#F1C40F", "desc": "안정감과 신뢰"},
    "금": {"color": "#95A5A6", "desc": "결단력과 원칙"},
    "수": {"color": "#3498DB", "desc": "지혜와 유연함"}
}

# 십성 매핑 함수 (변수명 규칙 준수: il_gan)
def get_ten_gods(il_gan, target):
    mapping = {
        ("금", "수"): "식상 (창의력/표현)",
        ("금", "화"): "관성 (규율/명예)",
        ("금", "목"): "재성 (결과/현실)",
        ("금", "토"): "인성 (수용/학습)",
        ("금", "금"): "비겁 (주관/경쟁)",
        ("목", "화"): "식상 (창의력/표현)",
        ("목", "금"): "관성 (규율/명예)",
        ("목", "토"): "재성 (결과/현실)",
        ("목", "수"): "인성 (수용/학습)",
        ("목", "목"): "비겁 (주관/경쟁)",
        # 타 오행은 확장 가능
    }
    return mapping.get((il_gan, target), "기타 기운")

# ================= 2. 시각화 컴포넌트 =================
class SajuVisualizer:
    @staticmethod
    def draw_element_pie(elements):
        # 오행 분포 파이 차트
        df = pd.DataFrame(list(elements.items()), columns=['오행', '점수'])
        fig = px.pie(df, values='점수', names='오행', 
                     color='오행', 
                     color_discrete_map={k: v['color'] for k, v in ELEMENT_INFO.items()},
                     hole=0.5)
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(showlegend=False, height=350, margin=dict(t=30, b=30, l=30, r=30))
        return fig

    @staticmethod
    def draw_strength_gauge(score):
        # 신강/신약 게이지 (이미지 느낌 재현)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "자아 에너지 강도", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [-50, 50], 'tickwidth': 1},
                'bar': {'color': "#2C3E50"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#D5DBDB",
                'steps': [
                    {'range': [-50, -15], 'color': '#EBF5FB'},
                    {'range': [-15, 15], 'color': '#F2F4F4'},
                    {'range': [15, 50], 'color': '#FEF9E7'}
                ],
            }
        ))
        fig.update_layout(height=280, margin=dict(t=50, b=20, l=30, r=30))
        return fig

# ================= 3. 해설 생성 엔진 =================
class AnalysisEngine:
    def __init__(self, name, elements, il_gan):
        self.name = name
        self.elements = elements
        self.il_gan = il_gan

    def generate_report(self):
        strong_elem = max(self.elements, key=self.elements.get)
        ten_god_name = get_ten_gods(self.il_gan, strong_elem)
        
        summary = f"### 🌟 {self.name} 학생의 타고난 성향: **[{ten_god_name}]**"
        
        detail = f"""
        {self.name} 학생은 **{self.il_gan}**의 본질을 가지고 태어났으며, 현재 사주에서 **{strong_elem}**의 기운이 가장 두드러집니다.
        
        이미지 분석 결과와 같이, 이러한 구조는 다음과 같은 학습 특징을 보입니다:
        
        1. **학습 스타일**: {ELEMENT_INFO[strong_elem]['desc']} 능력이 탁월합니다.
        2. **강점**: 주도적으로 문제를 해결하려는 의지가 강하며 목표 의식이 뚜렷합니다.
        3. **보완점**: {min(self.elements, key=self.elements.get)} 기운이 상대적으로 약해 뒷심이 부족할 수 있으니 체력 관리가 중요합니다.
        """
        return summary, detail

# ================= 4. 메인 어플리케이션 UI =================
def main():
    st.set_page_config(page_title="사주 학습 컨설팅 프로", layout="wide")

    # CSS 디자인
    st.markdown("""
        <style>
        .report-box {
            padding: 25px;
            border-radius: 15px;
            background-color: white;
            border: 1px solid #EAECEE;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background-color: #2C3E50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📚 AI 사주 기반 프리미엄 학습 분석")
    st.write("이미지 기반 고도화 알고리즘이 적용된 전문가용 리포트입니다.")

    # 사이드바 입력
    with st.sidebar:
        st.header("👤 학생 정보 입력")
        name = st.text_input("이름", "김준우")
        st.date_input("생년월일")
        st.time_input("출생시간")
        il_gan_input = st.selectbox("본인의 일간(본질)", ["금", "목", "화", "토", "수"])
        submit = st.button("전문 분석 시작")

    if submit:
        # 가상 분석 데이터 (이미지상의 수(水) 과다 및 신약 사주 케이스 재현)
        mock_elements = {"수": 52, "금": 18, "화": 12, "토": 10, "목": 8}
        strength_score = -12  # 신약 쪽으로 치우친 중립
        
        engine = AnalysisEngine(name, mock_elements, il_gan_input)
        summary, detail = engine.generate_report()

        # 레이아웃 구성
        col1, col2 = st.columns([1, 1.2])

        with col1:
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.subheader("🎯 오행 밸런스 결과")
            st.plotly_chart(SajuVisualizer.draw_element_pie(mock_elements), use_container_width=True)
            st.plotly_chart(SajuVisualizer.draw_strength_gauge(strength_score), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown(summary)
            st.markdown(detail)
            st.divider()
            
            # 이미지 스타일의 하단 팁
            st.info(f"💡 **전문가 제안**: {name} 학생은 '하얀 쥐'처럼 영특하지만 기운이 한곳으로 쏠려 있습니다. 수(水)의 지혜를 발휘할 수 있는 토론식 수업을 추천합니다.")
            
            # 행동 가이드
            guide_col1, guide_col2 = st.columns(2)
            guide_col1.success("**추천 과목**\n\n언어, 사회, 예술")
            guide_col2.warning("**환경 조성**\n\n습도 조절 및 파란색 소품")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
