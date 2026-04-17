import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ================= 1. 프롬프트 최적화 및 전문 해설 엔진 =================
# 실제 서비스 시에는 이 부분을 OpenAI API 등 LLM과 연동하게 됩니다.
# 여기서는 최적화된 프롬프트 로직을 기반으로 한 '고정밀 알고리즘'을 구현합니다.

class ProfessionalFortuneEngine:
    """명리학 전문가 페르소나를 가진 분석 엔진"""
    
    ELEMENT_DETAILS = {
        "목": {"title": "성장하는 나무", "color": "#2ECC71", "desc": "추진력과 호기심, 시작하는 에너지"},
        "화": {"title": "타오르는 불꽃", "color": "#E74C3C", "desc": "열정과 표현력, 화려한 몰입도"},
        "토": {"title": "단단한 대지", "color": "#F1C40F", "desc": "안정감과 신뢰, 묵직한 끈기"},
        "금": {"title": "정교한 바위", "color": "#95A5A6", "desc": "결단력과 논리, 원칙 중심의 사고"},
        "수": {"title": "흐르는 물", "color": "#3498DB", "desc": "지혜와 유연함, 깊은 통찰력"}
    }

    @staticmethod
    def get_ten_gods_analysis(il_gan, strong_elem):
        # 십성 기반 전문 분석 (이미지 퀄리티 재현)
        mapping = {
            ("금", "수"): "식상 (창의적 표현형)",
            ("금", "화"): "관성 (명예와 규율형)",
            ("금", "목"): "재성 (결과와 효율형)",
            ("금", "토"): "인성 (수용과 학습형)",
            ("금", "금"): "비겁 (주관과 경쟁형)"
        }
        return mapping.get((il_gan, strong_elem), "균형 잡힌 기운")

    def generate_expert_report(self, name, il_gan, elements, strength_score):
        strong_elem = max(elements, key=elements.get)
        ten_god = self.get_ten_gods_analysis(il_gan, strong_elem)
        
        # 최적화된 프롬프트 스타일의 스토리텔링
        report = {
            "intro": f"**{name}**님은 **{self.ELEMENT_DETAILS[il_gan]['title']}**의 본질을 품고, **{strong_elem}**의 에너지를 도구로 사용하는 구조입니다.",
            "main_analysis": f"사주 구성상 **{ten_god}**의 기운이 매우 강력합니다. 이는 단순히 재능이 많은 것을 넘어, 본인이 이해한 내용을 세상에 전달하거나 구체화할 때 삶의 만족도가 가장 높아짐을 의미합니다.",
            "strength_desc": f"자아 에너지 강도는 **{strength_score}**로, 주변 환경의 에너지를 흡수하여 본인의 것으로 만드는 '수용적 리더십'이 돋보입니다.",
            "action_plan": f"오늘의 정체된 에너지를 깨우기 위해 **화이트/실버** 계열의 아이템을 착용하시고, 부족한 **화(火)** 기운을 위해 따뜻한 성질의 음식을 섭취하세요."
        }
        return report

# ================= 2. 시각화 컴포넌트 (Plotly) =================
class SajuVisualizer:
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

# ================= 3. Streamlit UI 통합 레이아웃 =================
def main():
    st.set_page_config(page_title="점신 PRO - 통합 사주 리포트", layout="wide")

    # 고도화된 CSS 디자인
    st.markdown("""
        <style>
        .main { background-color: #F8F9FA; }
        .stCard {
            background-color: white; padding: 30px; border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 25px;
            border: 1px solid #F1F2F6;
        }
        .header-title { font-size: 32px; font-weight: 800; color: #2C3E50; letter-spacing: -1px; }
        .lucky-tag {
            display: inline-block; padding: 5px 15px; border-radius: 50px;
            background: #F1F2F6; color: #57606F; font-size: 14px; margin-right: 8px;
        }
        .expert-quote {
            font-style: italic; border-left: 4px solid #3498DB;
            padding-left: 15px; color: #2F3542; margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. 헤더 섹션
    st.markdown('<div class="header-title">🔮 통합 명리 컨설팅 대시보드</div>', unsafe_allow_html=True)
    st.write(f"최신 알고리즘 적용일: {datetime.now().strftime('%Y-%m-%d')}")

    # 2. 사이드바 - 사용자 입력
    with st.sidebar:
        st.header("📋 사용자 프로필")
        name = st.text_input("성함", "김준우")
        birth_date = st.date_input("생년월일", value=datetime(1983, 11, 8))
        birth_time = st.time_input("출생시간")
        il_gan = st.selectbox("본인의 일간(본질)", ["금", "수", "목", "화", "토"])
        st.divider()
        submit = st.button("전문 분석 리포트 생성")

    if submit:
        # 가상 데이터 생성 (이미지 및 전문가 분석값 재현)
        mock_elements = {"목": 10, "화": 15, "토": 10, "금": 12, "수": 53}
        strength_score = -12
        
        engine = ProfessionalFortuneEngine()
        report = engine.generate_expert_report(name, il_gan, mock_elements, strength_score)

        # 레이아웃 구성
        col1, col2 = st.columns([1, 1.4])

        with col1:
            # 오늘의 행운
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.subheader("🍀 오늘의 행운 처방")
            st.markdown('<span class="lucky-tag">🎨 컬러: 화이트</span><span class="lucky-tag">🔢 숫자: 4, 9</span>', unsafe_allow_html=True)
            st.markdown('<span class="lucky-tag">🍲 음식: 생강차</span><span class="lucky-tag">🧭 방향: 서쪽</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # 오행 그래프
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.subheader("📊 오행 에너지 밸런스")
            st.plotly_chart(SajuVisualizer.draw_radar(mock_elements), use_container_width=True)
            st.write(f"**수(水)** 기운이 매우 강한 사주입니다. 이는 깊은 지혜와 영리함을 뜻하지만, 동시에 감정의 기복을 다스리는 것이 핵심 과제입니다.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # 상세 해설 (최적화 프롬프트 반영)
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.markdown(f"### 📜 {name}님을 위한 심층 운세 리포트")
            
            st.markdown('<div class="expert-quote">' + report['intro'] + '</div>', unsafe_allow_html=True)
            
            tab1, tab2, tab3 = st.tabs(["💡 성향 및 학습", "💰 재물과 사회운", "📅 월간 흐름"])
            
            with tab1:
                st.write("#### 타고난 기질과 지능 패턴")
                st.write(report['main_analysis'])
                st.info(f"**전략:** {name}님은 단순 암기보다 '왜?'라는 원리를 깨우칠 때 뇌가 가장 활성화됩니다. 본인이 이해한 것을 남에게 설명하는 공부법을 추천합니다.")
            
            with tab2:
                st.write("#### 사회적 성취와 에너지 사용")
                st.write(report['strength_desc'])
                st.success("자신의 전문 기술을 활용해 독립적인 성취를 이루는 데 유리한 운세입니다. 올해는 특히 문서를 다루는 계약운이 좋습니다.")
            
            with tab3:
                st.write("#### 이번 달 주의사항")
                st.warning("감정적인 지출이 생길 수 있는 달입니다. 중요한 결정은 오후 1시에서 3시 사이(화 기운이 강한 시간)에 내리는 것이 유리합니다.")
            
            st.divider()
            st.subheader("👨‍🏫 전문가 총평")
            st.write(f"\"{name}님, 당신은 맑은 호수 위에 놓인 예리한 칼과 같습니다. 그 영리함을 세상의 가치로 바꾸기 위해선 '행동의 루틴'이 필요합니다. {report['action_plan']}\"")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
