import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ================= 1. 고급 명리 데이터 엔진 =================
ELEMENT_INFO = {
    "목": {"color": "#2ECC71", "desc": "추진력과 성장"},
    "화": {"color": "#E74C3C", "desc": "열정과 표현력"},
    "토": {"color": "#F1C40F", "desc": "안정감과 신뢰"},
    "금": {"color": "#95A5A6", "desc": "결단력과 원칙"},
    "수": {"color": "#3498DB", "desc": "지혜와 유연함"}
}

# 십성 매핑 로직 (일간 기준 관계 분석)
def get_ten_gods(il-gan, target):
    # 실제 앱에서는 일간의 음양오행과 타겟의 관계를 계산하는 복잡한 로직이 들어갑니다.
    # 예시: 일간이 금(庚)일 때 수(癸/壬)는 식상(식신/상관)입니다.
    mapping = {
        ("금", "수"): "식상 (창의력/표현)",
        ("금", "화"): "관성 (규율/명예)",
        ("금", "목"): "재성 (결과/현실)",
        ("금", "토"): "인성 (수용/학습)",
        ("금", "금"): "비겁 (주관/경쟁)"
    }
    return mapping.get((il-gan, target), "기타")

# ================= 2. 시각화 컴포넌트 (이미지 퀄리티 재현) =================
class SajuVisualizer:
    @staticmethod
    def draw_element_gauge(elements):
        # 이미지의 오행 분포 차트 재현
        df = pd.DataFrame(list(elements.items()), columns=['오행', '점수'])
        df['color'] = df['오행'].map(lambda x: ELEMENT_INFO[x]['color'])
        
        fig = px.pie(df, values='점수', names='오행', 
                     color='오행', color_discrete_map={k: v['color'] for k, v in ELEMENT_INFO.items()},
                     hole=0.6)
        fig.update_traces(textinfo='percent+label', hoverinfo='label+value')
        fig.update_layout(showlegend=False, height=300, margin=dict(t=0, b=0, l=0, r=0))
        return fig

    @staticmethod
    def draw_strength_meter(score):
        # 이미지의 신강/신약 게이지 재현
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "자아 에너지 강도 (신강/신약)"},
            gauge = {
                'axis': {'range': [-50, 50]},
                'bar': {'color': "#34495E"},
                'steps': [
                    {'range': [-50, -15], 'color': "#EBF5FB"},
                    {'range': [-15, 15], 'color': "#D5DBDB"},
                    {'range': 15, 50, 'color': "#FEF9E7"}
                ],
            }
        ))
        fig.update_layout(height=250, margin=dict(t=50, b=20))
        return fig

# ================= 3. 콘텐츠 생성기 (이미지 수준의 해설) =================
class ReportGenerator:
    def __init__(self, name, elements, il-gan):
        self.name = name
        self.elements = elements
        self.il_gan_type = il-gan
        
    def get_summary(self):
        # 이미지의 "타고난 성향" 텍스트 퀄리티 재현
        strong_elem = max(self.elements, key=self.elements.get)
        ten_god = get_ten_gods(self.il_gan_type, strong_elem)
        
        return f"""
        ### 🌟 {self.name} 학생의 핵심 학습 코드: **[{ten_god}]**
        {self.name} 학생은 **'{self.il_gan_type}'**의 기운을 바탕으로, **'{strong_elem}'**의 에너지를 도구로 사용하는 구조입니다. 
        이미지 분석 결과처럼 '식상'의 기운이 강할 경우, 단순 암기보다는 본인이 이해한 내용을 **글이나 말로 표현할 때** 학습 효율이 극대화됩니다.
        """

# ================= 4. 메인 UI (Streamlit) =================
st.set_page_config(page_title="프리미엄 사주 컨설팅", layout="wide")

# 스타일링
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stCard { 
        border-radius: 15px; 
        padding: 20px; 
        background: white; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .header-text { color: #2C3E50; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ AI 사주 기반 맞춤형 학습 리포트")

with st.sidebar:
    st.header("입력 정보")
    name = st.text_input("이름", "김준우")
    birth = st.date_input("생년월일")
    time = st.time_input("출생시간")
    il_gan = st.selectbox("본인의 일간 (일주 천간)", ["금", "목", "화", "토", "수"])

if st.button("전문 리포트 생성"):
    # 가상 데이터 산출 (이미지 기반)
    mock_elements = {"수": 45, "화": 15, "토": 10, "금": 20, "목": 10}
    strength_score = -5 # 이미지의 0점대에 근접한 신약/중립 사주 가정
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("📊 오행 분포 분석")
        st.plotly_chart(SajuVisualizer.draw_element_gauge(mock_elements), use_container_width=True)
        st.plotly_chart(SajuVisualizer.draw_strength_meter(strength_score), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        report = ReportGenerator(name, mock_elements, il_gan)
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown(report.get_summary(), unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📝 정밀 분석 결과")
        cols = st.columns(2)
        cols[0].info("**타고난 성향 (식신/상관)**\n\n두뇌 회전이 빠르고 창의적입니다. 틀에 박힌 공부보다 스스로 원리를 깨우치는 방식이 적합합니다.")
        cols[1].warning("**주의해야 할 점 (관성 부족)**\n\n집중력이 순간적으로 높으나 마무리가 약할 수 있습니다. 짧은 시간 단위의 계획표가 필수적입니다.")
        
        st.success(f"💡 **{name} 학생을 위한 전략:** 하얀 쥐의 영리함과 수(水)의 유연함을 살려 '설명하는 공부법'을 도입하세요.")
        st.markdown('</div>', unsafe_allow_html=True)
