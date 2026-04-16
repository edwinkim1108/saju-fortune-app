import streamlit as st
from datetime import datetime
import random
import os
from io import BytesIO

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

# ================= 강약 =================
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

# ================= 학습 성향 =================
def 학습_성향(strong):
    return {
        "목":"이해 중심 학습형 (개념 연결 능력 우수)",
        "화":"몰입형 학습 (단기 집중력 매우 강함)",
        "토":"꾸준형 학습 (장기 성적 상승형)",
        "금":"문제풀이형 (시험 대응 능력 우수)",
        "수":"암기+이해 혼합형 (균형형 학습)"
    }.get(strong)

# ================= 십성 해석 =================
def 십성_해석(strong):
    return {
        "목":"인성 발달 → 이해력, 학습 흡수력 높음",
        "화":"식상 발달 → 문제풀이, 표현력 강함",
        "토":"재성 발달 → 결과 중심, 성적 집착형",
        "금":"관성 발달 → 집중력, 관리 능력 우수",
        "수":"인성+식상 혼합 → 균형형 인재"
    }.get(strong)

# ================= 과목 연결 =================
def 과목_추천(strong):
    return {
        "목":"국어/영어 독해형 과목 강점",
        "화":"발표/토론/회화형 과목 강점",
        "토":"암기형 과목 안정적",
        "금":"수학/과학 문제풀이 강점",
        "수":"전과목 균형형"
    }.get(strong)

# ================= 대운 =================
def 대운_분석():
    return [
        "10~19세: 학습 기반 형성기",
        "20~29세: 진로 결정기",
        "30~39세: 성장 및 확장기",
        "40~49세: 안정 및 축적기"
    ]

# ================= 오늘 운 =================
def 오늘_운():
    return random.randint(60,95)

# ================= PDF =================
def create_pdf(name, text):
    buffer = BytesIO()
    font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")

    if not os.path.exists(font_path):
        return None

    pdfmetrics.registerFont(TTFont("Nanum", font_path))

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "Nanum"

    text = text.replace("\n","<br/>")
    content = [Paragraph(text, styles["Normal"])]

    doc.build(content)
    buffer.seek(0)

    return buffer

# ================= UI =================
st.set_page_config(page_title="학생 사주 분석 앱", layout="centered")
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

    # 오행
    elements = 오행_카운트(사주)
    strong, weak, level = 강약_분석(elements)

    st.subheader("🌿 오행 분석")
    st.write(elements)
    st.write(f"💪 강한 오행: {strong}")
    st.write(f"⚠️ 약한 오행: {weak}")
    st.write(f"📊 균형 상태: {level}")

    # 학습
    st.subheader("🧠 학습 성향")
    st.success(학습_성향(strong))

    # 십성
    st.subheader("⚡ 십성 해석")
    st.info(십성_해석(strong))

    # 과목
    st.subheader("📚 과목 추천")
    st.write(과목_추천(strong))

    # 대운
    st.subheader("🌊 대운 흐름")
    for d in 대운_분석():
        st.write(d)

    # 오늘 운
    st.subheader("📊 오늘 공부 운")
    today = 오늘_운()
    st.metric("집중력", f"{today}%")
    st.progress(today)

    # PDF
    text = f"""
    이름: {name}

    사주: {사주}
    오행: {elements}

    강한 오행: {strong}
    약한 오행: {weak}
    균형: {level}

    학습 성향: {학습_성향(strong)}
    십성: {십성_해석(strong)}
    과목: {과목_추천(strong)}
    """

    pdf = create_pdf(name, text)

    if pdf:
        st.download_button("📄 PDF 다운로드", pdf, file_name="학생_리포트.pdf")
    else:
        st.error("⚠️ NanumGothic.ttf 필요")