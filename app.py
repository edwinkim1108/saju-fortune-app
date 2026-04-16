import streamlit as st
from datetime import datetime
import random
import os
from io import BytesIO

# 그래프
import matplotlib.pyplot as plt
import numpy as np

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ================= 기본 데이터 =================
천간 = ["갑","을","병","정","무","기","경","신","임","계"]
지지 = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

오행_map = {
    "갑":"목","을":"목","병":"화","정":"화",
    "무":"토","기":"토","경":"금","신":"금",
    "임":"수","계":"수",
    "자":"수","축":"토","인":"목","묘":"목",
    "진":"토","사":"화","오":"화","미":"토",
    "신":"금","유":"금","술":"토","해":"수"
}

# ================= 사주 계산 =================
def get_간지(year, month, day, hour):
    년주 = 천간[(year-4)%10] + 지지[(year-4)%12]
    월주 = 천간[(year+month)%10] + 지지[(month)%12]
    일주 = 천간[(year+month+day)%10] + 지지[(day)%12]
    시주 = 천간[(day+hour)%10] + 지지[(hour)%12]
    return 년주, 월주, 일주, 시주

# ================= 오행 분석 =================
def 오행_카운트(사주):
    elements = {"목":0,"화":0,"토":0,"금":0,"수":0}
    for g in 사주:
        for ch in g:
            elements[오행_map[ch]] += 1
    return elements

def 강약_분석(elements):
    strong = max(elements, key=elements.get)
    weak = min(elements, key=elements.get)
    imbalance = elements[strong] - elements[weak]

    if imbalance >= 3:
        level = "극단 불균형"
    elif imbalance == 2:
        level = "불균형"
    else:
        level = "균형형"

    return strong, weak, level

# ================= 전문가 해설 =================
def 오행_해설(elements, strong, weak):
    detail = {
        "목": "목은 성장과 확장을 의미하며 이해력과 사고력과 연결됩니다.",
        "화": "화는 집중력과 에너지로 몰입 학습과 관련됩니다.",
        "토": "토는 안정성과 반복으로 꾸준함과 관련됩니다.",
        "금": "금은 규칙과 구조로 문제풀이 능력과 연결됩니다.",
        "수": "수는 기억과 사고로 암기력과 관련됩니다."
    }

    return f"""
이 사주는 {strong} 기운이 강하게 작용합니다.

👉 {strong} 특징: {detail[strong]}

반면 {weak} 기운이 부족하여 해당 영역은 약점이 될 수 있습니다.

👉 {weak} 부족 영향: {detail[weak]}

👉 핵심 전략: 강점 활용 + 약점 보완
"""

def 학습_스토리(strong, weak):
    return f"""
이 학생은 {strong} 중심 학습 구조입니다.

👉 {strong} 기반 공부에서는 빠른 성과  
👉 {weak} 기반 공부에서는 효율 저하

👉 맞는 공부법이 성적을 결정합니다.
"""

def 총평(strong, weak):
    return f"""
이 사주는 {strong} 중심 구조입니다.

강점을 활용하면 빠르게 성장하지만  
{weak} 부족은 장기 안정성을 떨어뜨립니다.

👉 결론: 전략적 공부 필수
"""

def 행동_가이드(strong, weak):
    guide = {
        "목":"개념 중심 학습",
        "화":"짧고 강한 집중",
        "토":"반복과 꾸준함",
        "금":"문제풀이 중심",
        "수":"암기 반복"
    }

    return f"""
✔ 추천 공부법: {guide[strong]}
✔ 보완 전략: {guide[weak]}

👉 강점 70% + 약점 30% 전략
"""

# ================= 그래프 =================
def 육각형_그래프(elements):
    labels = list(elements.keys())
    values = list(elements.values())

    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("오행 균형 그래프")

    return fig

# ================= PDF =================
def create_pdf(name, 사주, elements, strong, weak, 해설, 총평_text, 가이드):
    buffer = BytesIO()
    font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")

    if not os.path.exists(font_path):
        return None

    pdfmetrics.registerFont(TTFont("Nanum", font_path))

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    for s in styles.byName.values():
        s.fontName = "Nanum"

    content = []

    def add(text):
        content.append(Paragraph(text.replace("\n","<br/>"), styles["Normal"]))

    add(f"<b>{name} 학생 사주 분석 리포트</b><br/><br/>")
    add(f"<b>사주:</b> {사주}<br/><br/>")
    add(f"<b>오행:</b> {elements}<br/>강:{strong} / 약:{weak}<br/><br/>")
    add(f"<b>오행 해설</b><br/>{해설}<br/><br/>")
    add(f"<b>총평</b><br/>{총평_text}<br/><br/>")
    add(f"<b>학습 전략</b><br/>{가이드}<br/><br/>")

    doc.build(content)
    buffer.seek(0)
    return buffer

# ================= UI =================
st.set_page_config(page_title="학생 사주 분석", layout="centered")
st.title("📚 학생 사주 기반 학습 분석 앱")

with st.form("form"):
    year = st.number_input("출생년도", 2000, 2025, 2010)
    month = st.number_input("월",1,12,6)
    day = st.number_input("일",1,31,15)
    hour = st.number_input("시간",0,23,12)
    name = st.text_input("이름")

    submit = st.form_submit_button("분석하기")

if submit:
    년주, 월주, 일주, 시주 = get_간지(year,month,day,hour)
    사주 = [년주,월주,일주,시주]

    st.subheader("🔮 사주팔자")
    st.write(f"{년주} / {월주} / {일주} / {시주}")

    elements = 오행_카운트(사주)
    strong, weak, level = 강약_분석(elements)

    st.subheader("🌿 오행 분석")
    st.write(elements)
    st.write(f"강한 오행: {strong}")
    st.write(f"약한 오행: {weak}")
    st.write(f"균형 상태: {level}")

    st.subheader("📊 오행 시각화")
    st.pyplot(육각형_그래프(elements))

    st.subheader("📖 오행 해설")
    st.info(오행_해설(elements, strong, weak))

    st.subheader("🧠 학습 해설")
    st.success(학습_스토리(strong, weak))

    st.subheader("🔮 총평")
    st.warning(총평(strong, weak))

    st.subheader("📌 행동 가이드")
    st.error(행동_가이드(strong, weak))

    st.subheader("📊 오늘 공부 운")
    today = random.randint(60,95)
    st.metric("집중력", f"{today}%")
    st.progress(today)

    # PDF
    pdf = create_pdf(
        name,
        사주,
        elements,
        strong,
        weak,
        오행_해설(elements, strong, weak),
        총평(strong, weak),
        행동_가이드(strong, weak)
    )

    if pdf:
        st.download_button("📄 프리미엄 PDF 다운로드", pdf, file_name=f"{name}_리포트.pdf")
    else:
        st.error("⚠️ NanumGothic.ttf 파일 필요")