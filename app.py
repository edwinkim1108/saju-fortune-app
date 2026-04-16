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
    월주 = 천간[(month)%10] + 지지[(month)%12]
    일주 = 천간[(day)%10] + 지지[(day)%12]
    시주 = 천간[(hour)%10] + 지지[(hour)%12]
    return 년주, 월주, 일주, 시주

# ================= 오행 분석 =================
def 오행_카운트(사주):
    elements = {"목":0,"화":0,"토":0,"금":0,"수":0}
    for g in 사주:
        for ch in g:
            elements[오행_map[ch]] += 1
    return elements

# ================= 강약 =================
def 강약(elements):
    strong = max(elements, key=elements.get)
    weak = min(elements, key=elements.get)
    return strong, weak

# ================= 학습 구조 =================
def 학습_분석(strong):
    return {
        "목":"개념형 (이해력 중심)",
        "화":"몰입형 (집중력 중심)",
        "토":"꾸준형 (지속력 중심)",
        "금":"문제풀이형 (시험형)",
        "수":"암기형 (기억력)"
    }.get(strong)

# ================= 십성 =================
def 십성_간단(strong):
    return {
        "목":"인성 발달 → 이해력 우수",
        "화":"식상 발달 → 표현력/문제풀이",
        "토":"재성 발달 → 결과 중심",
        "금":"관성 발달 → 집중력/관리력",
        "수":"인성+식상 → 균형형"
    }.get(strong)

# ================= 대운 =================
def 대운():
    return [f"{i*10}세 ~ {i*10+9}세 변화기" for i in range(1,9)]

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
st.set_page_config(page_title="학생 사주 공부 앱", layout="centered")
st.title("📚 학생 전용 사주 공부 분석 앱")

with st.form("form"):
    year = st.number_input("출생년도", 2000, 2025, 2010)
    month = st.number_input("월",1,12,6)
    day = st.number_input("일",1,31,15)
    hour = st.number_input("시간",0,23,12)
    name = st.text_input("이름")
    submit = st.form_submit_button("분석")

if submit:

    년주, 월주, 일주, 시주 = get_간지(year,month,day,hour)
    사주 = [년주,월주,일주,시주]

    st.subheader("🔮 사주팔자")
    st.write(f"{년주} / {월주} / {일주} / {시주}")

    # 오행
    elements = 오행_카운트(사주)
    strong, weak = 강약(elements)

    st.subheader("🌿 오행 분석")
    st.write(elements)
    st.write(f"강한 오행: {strong}")
    st.write(f"약한 오행: {weak}")

    # 학습
    st.subheader("🧠 학습 성향")
    st.success(학습_분석(strong))

    # 십성
    st.subheader("⚡ 십성 분석")
    st.info(십성_간단(strong))

    # 과목
    st.subheader("📚 과목 추천")
    st.write(f"{strong} 기반 과목 강점")

    # 대운
    st.subheader("🌊 인생 흐름 (대운)")
    for d in 대운():
        st.write(d)

    # 오늘 운세
    st.subheader("📊 오늘 공부 운")
    st.metric("집중력", f"{random.randint(60,95)}%")

    # PDF
    text = f"""
    이름: {name}
    사주: {사주}

    오행: {elements}
    강점: {strong}
    약점: {weak}

    학습 유형: {학습_분석(strong)}
    십성: {십성_간단(strong)}
    """

    pdf = create_pdf(name, text)

    if pdf:
        st.download_button("📄 PDF 다운로드", pdf, file_name="리포트.pdf")
    else:
        st.error("폰트 파일 필요 (NanumGothic.ttf)")