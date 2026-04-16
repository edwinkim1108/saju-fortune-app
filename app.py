import streamlit as st
import random
from io import BytesIO
import os

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ================= 로그인 =================
if "login" not in st.session_state:
    st.session_state.login = False

def login():
    st.title("🔐 로그인")
    user = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if user == "admin" and pw == "1234":
            st.session_state.login = True
            st.success("로그인 성공")
        else:
            st.error("로그인 실패")

if not st.session_state.login:
    login()
    st.stop()

# ================= 기본 데이터 =================
천간 = ["갑","을","병","정","무","기","경","신","임","계"]
지지 = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

# ================= 오행 =================
def 오행_분석(일간):
    return {
        "갑":"목","을":"목","병":"화","정":"화",
        "무":"토","기":"토","경":"금","신":"금",
        "임":"수","계":"수"
    }.get(일간)

# ================= 학습 구조 =================
def 학습_구조_분석(일간):
    구조 = {
        "목": {"type":"이해형","strength":"개념 연결 능력 우수","weak":"암기 약함"},
        "화": {"type":"몰입형","strength":"집중력 강함","weak":"지속력 부족"},
        "토": {"type":"꾸준형","strength":"지속력 강함","weak":"속도 느림"},
        "금": {"type":"문제풀이형","strength":"시험형 문제 강함","weak":"개념 부족 위험"},
        "수": {"type":"암기형","strength":"기억력 뛰어남","weak":"집중력 기복"}
    }
    return 구조.get(오행_분석(일간))

# ================= 과목 성향 =================
def 과목_성향(오행):
    if 오행 == "목":
        return {"국어":"독해 강점","영어":"이해력 우수","수학":"개념형 문제 강함"}
    elif 오행 == "화":
        return {"국어":"속독 강점","영어":"회화 강점","수학":"속도 빠름"}
    elif 오행 == "토":
        return {"국어":"꾸준 상승","영어":"암기 안정","수학":"기본기 강함"}
    elif 오행 == "금":
        return {"국어":"비문학 강점","영어":"문법 정확","수학":"문제풀이 최강"}
    else:
        return {"국어":"감각적 이해","영어":"암기 강점","수학":"응용 강함"}

# ================= 부모 코칭 =================
def 부모_코칭(일간):
    return {
        "갑":["목표 제시형 지도","자율성 중요"],
        "을":["습관 형성 중요","꾸준함 칭찬"],
        "병":["짧은 목표 반복","즉각 피드백"],
        "경":["문제풀이 중심 지도","경쟁 활용"],
        "계":["암기 환경 제공","반복 체크"]
    }.get(일간, ["루틴 유지","기본기 강화"])

# ================= 전략 =================
def 성적_상승_전략(일간):
    return {
        "경":"문제풀이 70% 전략",
        "계":"암기 집중 전략",
        "병":"짧고 강한 공부",
        "을":"꾸준함 유지",
        "임":"이해 중심 학습"
    }.get(일간, "기본기 + 반복")

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
    styles["Title"].fontName = "Nanum"
    styles["BodyText"].fontName = "Nanum"

    content = []
    content.append(Paragraph(f"{name} 학생 분석 리포트", styles["Title"]))
    content.append(Paragraph("<br/>", styles["Normal"]))

    text = text.replace("\n", "<br/>")
    content.append(Paragraph(text, styles["BodyText"]))

    doc.build(content)
    buffer.seek(0)

    return buffer

# ================= UI =================
st.set_page_config(page_title="📚 공부 사주 코칭", layout="centered")

st.title("📚 학생 사주 기반 공부 코칭 앱")

with st.form("form"):
    year = st.number_input("출생년도", 2000, 2025, 2010)
    month = st.number_input("월", 1, 12, 6)
    day = st.number_input("일", 1, 31, 15)
    name = st.text_input("이름")

    submit = st.form_submit_button("분석하기")

if submit:
    일주 = 천간[(day)%10] + 지지[(day)%12]
    일간 = 일주[0]

    오행 = 오행_분석(일간)
    구조 = 학습_구조_분석(일간)
    과목 = 과목_성향(오행)

    st.success(f"{name} 학생 분석 결과")

    # 핵심 분석
    st.markdown("## 🧠 사주 기반 학습 구조 분석")
    st.write(f"👉 오행: **{오행}**")
    st.write(f"📌 유형: {구조['type']}")
    st.write(f"💪 강점: {구조['strength']}")
    st.write(f"⚠️ 약점: {구조['weak']}")

    # 과목
    st.markdown("## 📚 과목별 성향")
    for k, v in 과목.items():
        st.write(f"{k} → {v}")

    # 전략
    st.markdown("## 📈 성적 상승 전략")
    st.success(성적_상승_전략(일간))

    # 부모
    st.markdown("## 👨‍👩‍👧 부모 코칭")
    for c in 부모_코칭(일간):
        st.write(f"👉 {c}")

    # 컨디션
    st.markdown("## 📊 오늘 컨디션")
    집중 = random.randint(60,95)
    st.metric("집중력", f"{집중}%")
    st.progress(집중)

    st.info("👉 이 학생은 맞는 학습법 적용 시 성적 상승 가능성이 매우 높은 구조입니다.")

    # PDF
    text = f"""
    [핵심 분석]
    오행: {오행}
    유형: {구조['type']}
    강점: {구조['strength']}
    약점: {구조['weak']}

    [과목 성향]
    {과목}

    [전략]
    {성적_상승_전략(일간)}
    """

    pdf = create_pdf(name, text)

    if pdf:
        st.download_button(
            label="📄 PDF 리포트 다운로드",
            data=pdf,
            file_name=f"{name}_리포트.pdf",
            mime="application/pdf"
        )
    else:
        st.error("⚠️ NanumGothic.ttf 폰트 파일 필요")