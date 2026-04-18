import streamlit as st
import plotly.graph_objects as go
import hashlib
from datetime import datetime

# ================= 1. 방대한 명리 지식 베이스 (Expert System DB) =================

KAN_DETAILS = {
    "갑": { 
        "title": "하늘을 향해 뻗는 거목 (甲木)",
        "personality": "독립심과 추진력이 매우 강하며, 기질적으로 리더의 자질을 타고났습니다. 굽히기보다는 직접 돌파하는 성격입니다.",
        "strength": "한 번 정한 목표에 대한 집중력이 뛰어나며 대범한 기개를 가졌습니다.",
        "weakness": "융통성이 부족해 보일 수 있으며, 실패 시 좌절감이 다른 이들보다 크게 다가올 수 있습니다."
    },
    "을": { 
        "title": "생명력을 품은 유연한 덩굴 (乙木)",
        "personality": "겉으로는 부드러워 보이나 내면은 끈질긴 생명력과 적응력을 가지고 있습니다. 환경 변화에 민감하고 실속이 있습니다.",
        "strength": "세밀한 관찰력과 대인관계에서의 유연함이 돋보입니다.",
        "weakness": "자신의 주관을 겉으로 잘 드러내지 않아 속내를 알기 어렵고 우유부단하게 보일 수 있습니다."
    },
    "병": { 
        "title": "세상을 비추는 강렬한 태양 (丙火)",
        "personality": "화끈하고 정열적이며 매사에 긍정적입니다. 숨김이 없고 솔선수범하여 주변에 활기를 불어넣는 에너자이저입니다.",
        "strength": "도전 정신이 강하고 표현력이 풍부하여 예술이나 방송 분야에 두각을 나타냅니다.",
        "weakness": "성격이 급해 실수를 할 수 있으며 감정 기복이 다소 큰 편입니다."
    },
    "정": { 
        "title": "어둠을 밝히는 은은한 촛불 (丁火)",
        "personality": "따뜻하고 배려심이 깊으며 내면이 매우 치밀하고 섬세합니다. 헌신적이고 예술적인 감수성이 풍부합니다.",
        "strength": "한 분야를 깊이 파고드는 연구심과 정밀한 분석 능력이 전문 영역에서 빛을 발합니다.",
        "weakness": "예민한 감각으로 인해 스트레스를 잘 받으며 소심해질 때가 있습니다."
    },
    "무": { 
        "title": "모든 것을 품는 광활한 대지 (戊土)",
        "personality": "듬직하고 신뢰감이 있으며 변화에 흔들리지 않는 굳건함을 가졌습니다. 중재 능력이 좋고 포용력이 큽니다.",
        "strength": "안정적인 현실 감각과 책임감이 뛰어나 조직의 기틀을 잡는 데 능합니다.",
        "weakness": "다소 고집스럽고 보수적일 수 있으며 행동이 신중한 만큼 느릿하게 보일 수 있습니다."
    },
    "기": { 
        "title": "생명을 길러내는 옥토 (己土)",
        "personality": "성실하고 알뜰하며 세심한 성격입니다. 남을 챙기는 마음이 지극하고 교육이나 관리 업무에 적합합니다.",
        "strength": "실리를 챙기는 감각이 탁월하고 실수가 적으며 맡은 일을 끝까지 완수합니다.",
        "weakness": "의심이 많고 생각이 너무 깊어 기회를 놓치는 경우가 종종 있습니다."
    },
    "경": { 
        "title": "강직한 기운의 무쇠와 원석 (庚金)",
        "personality": "의리가 깊고 결단력이 있으며 공과 사를 아주 엄격히 구분합니다. 원칙을 중시하고 불의를 참지 못합니다.",
        "strength": "검경, 법률, 군사 계통이나 강력한 구조가 필요한 조직에서 최고의 능력을 보입니다.",
        "weakness": "지나치게 강압적이거나 차가운 인상을 줄 수 있어 인간관계에서 적을 만들기 쉽습니다."
    },
    "신": { 
        "title": "눈부시게 연마된 보석과 칼날 (辛金)",
        "personality": "섬세하고 날카로우며 깔끔한 성품입니다. 완벽주의자 성향이 강하고 미적 감각이 매우 뛰어납니다.",
        "strength": "정밀 기술, IT, 디자인 등 전문적인 분야에서 독보적인 정확성을 보여줍니다.",
        "weakness": "자존감이 매우 높아 주변의 비판에 과하게 민감하게 반응할 수 있습니다."
    },
    "임": { 
        "title": "모든 물을 받아들이는 대양 (壬水)",
        "personality": "지혜롭고 통찰력이 깊으며 만물을 포용하는 넓은 마음을 가졌습니다. 유연한 사고로 상황 대처 능력이 좋습니다.",
        "strength": "기획력과 경영 능력이 출중하며 거시적인 안목으로 미래를 내다봅니다.",
        "weakness": "방랑기가 있고 감추는 것이 많아 비밀스럽다는 평을 듣기 쉽습니다."
    },
    "계": { 
        "title": "하늘에서 내리는 지혜로운 이슬 (癸水)",
        "personality": "유연하고 임기응변에 능하며 지적 탐구심이 매우 강합니다. 조용하지만 내실이 깊은 전략가 타입입니다.",
        "strength": "상대방의 마음을 읽는 심리적 통찰력과 학문에 대한 깊은 이해도가 높습니다.",
        "weakness": "환경의 영향을 너무 많이 받으며 정서적으로 다소 불안정할 수 있습니다."
    }
}

ELEMENT_ADVICE = {
    "목": {
        "excess": "주관이 너무 강해 독단적일 수 있으니 타인의 의견을 경청하는 연습이 필요합니다.",
        "lack": "추진력이 부족할 수 있으니 작은 목표부터 실행하는 습관을 들여 에너지를 키우세요."
    },
    "화": {
        "excess": "감정 조절에 유의하고 서두르는 습관을 버려 마음의 평화를 찾는 것이 중요합니다.",
        "lack": "열정과 활동성이 떨어질 수 있으니 운동이나 활동적인 취미로 에너지를 보충하세요."
    },
    "토": {
        "excess": "생각이 너무 많아 행동이 지체될 수 있으니 신속한 의사결정 연습이 필요합니다.",
        "lack": "기초가 흔들릴 수 있으니 원칙을 지키고 신뢰를 쌓는 일에 집중하세요."
    },
    "금": {
        "excess": "주변에 너무 날카로운 태도를 보이지 않도록 부드러운 대화 기법을 익히세요.",
        "lack": "맺고 끊음이 약할 수 있으니 냉철한 판단이 필요한 순간에는 과감해져야 합니다."
    },
    "수": {
        "excess": "생각이 한 곳에 정체되지 않도록 야외 활동을 통해 기분을 전환하세요.",
        "lack": "지혜와 인내가 부족하게 느껴질 때 명상이나 독서를 통해 내실을 다지세요."
    }
}

# ================= 2. 하이엔드 로컬 엔진 (Local Engine Core) =================

def get_local_analysis(name, gender, b_date, b_time):
    # 결정론적 해시값 생성
    seed_str = f"{b_date}{b_time}{gender}{name}"
    h_int = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    
    # 일간 선정
    kan_keys = list(KAN_DETAILS.keys())
    il_gan = kan_keys[h_int % 10]
    kan_data = KAN_DETAILS[il_gan]
    
    # 오행 점수 계산
    elements = {
        "목": (h_int % 20) + 15,
        "화": ((h_int >> 4) % 20) + 15,
        "토": ((h_int >> 8) % 20) + 15,
        "금": ((h_int >> 12) % 20) + 15,
        "수": ((h_int >> 16) % 20) + 15
    }
    
    # 자아 강도
    strength = (h_int % 61) - 30
    
    max_elem = max(elements, key=elements.get)
    min_elem = min(elements, key=elements.get)
    
    # 리포트 생성
    report = f"""
## **[천부적 기질과 성품 - 오행(五行)의 미학]**

{name} 님의 타고난 기운은 **{kan_data['title']}**입니다. 
명리학적 관점에서 볼 때, 귀하는 **{kan_data['personality']}**라는 독특한 성품을 가졌습니다. 

특히 이 기운의 에너지가 귀하의 자아를 형성하는 주된 동력입니다.
- **주요 강점:** {kan_data['strength']}
- **보완할 점:** {kan_data['weakness']}

## **[에너지 밸런스와 오행의 상호작용]**

귀하의 오행 분포를 정밀 분석한 결과, **{max_elem}**의 기운이 가장 왕성하고 **{min_elem}**의 기운이 다소 부족한 상태입니다.

- **{max_elem} 기운의 영향:** {ELEMENT_ADVICE[max_elem]['excess']}
- **{min_elem} 기운의 보충 전략:** {ELEMENT_ADVICE[min_elem]['lack']}

## **[재물운과 사회적 성취 - 비즈니스 명리]**

귀하는 조직 내에서 탁월한 적응력을 보이거나, 혹은 독보적인 전문성을 발휘하여 재물을 모으는 재능이 있음을 시사합니다.

- **최적의 직업군:** {"리더쉽이 필요한 경영, 전문 기술, 창업 분야" if strength > 0 else "전략적 기획, 행정 관리, 전문 컨설팅 분야"}
- **재물운 조언:** 꾸준히 실속을 챙기는 관리 능력이 뛰어나므로, 장기적인 자산 가치 상승에 집중하는 것이 유리합니다.
    """
    
    return {
        "il_gan": il_gan,
        "il_gan_title": kan_data['title'],
        "elements": elements,
        "self_strength": strength,
        "report": report
    }

# ================= 3. 프리미엄 UI =================

def main():
    st.set_page_config(page_title="Expert 명리 기질 분석 & 학습 컨설팅", layout="wide")
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;800&display=swap');
        html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
        .main-card { background: #ffffff; padding: 40px; border-radius: 25px; border: 1px solid #f0f0f0; box-shadow: 0 10px 30px rgba(0,0,0,0.03); margin-bottom: 20px;}
        .report-header { font-size: 30px; font-weight: 800; color: #1e272e; margin-bottom: 30px; border-left: 8px solid #1e272e; padding-left: 20px; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("📋 학생 정보 등록")
        name = st.text_input("성함/학생 이름", "김준우")
        gender = st.radio("성별", ["남성", "여성"])
        b_date = st.date_input("생년월일", value=datetime(1983, 11, 8))
        b_time = st.text_input("태어난 시간 (24시간제)", value="00:00")
        
        st.divider()
        st.caption("※ 본 앱은 로컬 전문가 시스템(Zero-API)으로 작동하며, 데이터는 외부로 전송되지 않습니다.")
        run_analysis = st.button("전문 컨설팅 리포트 발행")

    if run_analysis:
        with st.spinner("전문가 시스템이 천기를 분석하고 있습니다..."):
            result = get_local_analysis(name, gender, b_date, b_time)
        
        if result:
            col1, col2 = st.columns([1, 1.6])

            with col1:
                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.subheader("📊 기질 에너지 맵")
                fig = go.Figure(data=go.Scatterpolar(
                    r=list(result['elements'].values()), 
                    theta=list(result['elements'].keys()),
                    fill='toself', fillcolor='rgba(30, 39, 46, 0.1)', line_color='#1e272e'
                ))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), showlegend=False, margin=dict(t=20, b=20, l=40, r=40))
                st.plotly_chart(fig, use_container_width=True)
                
                strength = result['self_strength']
                st.write(f"**자아 에너지 강도:** {'신강(주도적)' if strength > 0 else '신약(협력적)'} ({strength})")
                st.progress((strength + 30) / 60)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="main-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="report-header">{name} 학생 기질 분석 보고서</div>', unsafe_allow_html=True)
                st.markdown(f"**기본 기질:** {result['il_gan_title']}")
                st.divider()
                st.markdown(result['report'])
                st.divider()
                st.caption("Expert Myeong-Ri Analysis Engine v3.0 (Zero-API)")
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
