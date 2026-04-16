import streamlit as st
from datetime import datetime
import random
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

# ================= 공부 타입 =================
def 공부_타입(ilgan):
    return {
        "갑":"개념형","을":"반복형","병":"몰입형","정":"정리형",
        "무":"지속형","기":"계획형","경":"문제풀이형","신":"정확형",
        "임":"이해형","계":"암기형"
    }.get(ilgan)

# ================= 풀이 =================
def 공부_풀이(ilgan):
    data = {
        "갑": {"core":"성장과 확장","study":"개념 이해 강함","real":"설명하며 공부 시 성과 상승"},
        "을": {"core":"꾸준함","study":"반복 학습 강함","real":"장기 학습에서 성적 상승"},
        "병": {"core":"집중력","study":"몰입형","real":"짧고 강한 공부 효과적"},
        "정": {"core":"디테일","study":"정확성 높음","real":"오답노트 효과 최고"},
        "경": {"core":"분석력","study":"문제풀이 강함","real":"수학 상위권 가능"},
        "신": {"core":"정밀함","study":"실수 적음","real":"정확도 기반 성적 상승"},
        "임": {"core":"이해력","study":"응용 강함","real":"심화 문제 유리"},
        "계": {"core":"암기력","study":"반복 강함","real":"단어/공식 암기 강점"},
        "무": {"core":"지속력","study":"꾸준형","real":"시간 투자형 성과"},
        "기": {"core":"계획력","study":"체계적","real":"플래너 활용 필수"}
    }
    return data.get(ilgan)

# ================= 약점 =================
def 약점_분석(ilgan):
    return {
        "병":"지루함 약함",
        "계":"이해 부족 위험",
        "경":"개념 부족 시 약함",
        "을":"속도 느림"
    }.get(ilgan, "균형형")

# ================= 부모 코칭 =================
def 부모_코칭(ilgan):
    return {
        "갑":["목표 중심 지도","자율성 부여"],
        "을":["습관 형성 중요","꾸준함 칭찬"],
        "병":["짧은 목표 반복","칭찬 필수"],
        "경":["문제풀이 강조","경쟁 환경"],
        "계":["암기 환경 제공","반복 체크"]
    }.get(ilgan, ["기본기 강화","루틴 유지"])

# ================= 성적 전략 =================
def 성적_상승_전략(ilgan):
    return {
        "경":"문제풀이 70%",
        "계":"암기 집중 전략",
        "병":"짧고 강하게",
        "을":"꾸준함 유지",
        "임":"이해 중심"
    }.get(ilgan, "기본기 + 반복")

# ================= PDF =================
def create_pdf(name, text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph(f"{name} 학생 리포트", styles["Title"]))
    content.append(Paragraph(text, styles["BodyText"]))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ================= UI =================
st.set_page_config(page_title="📚 공부 사주 앱", layout="centered")

st.title("📚 학생 사주 공부 코칭 앱")

with st.form("form"):
    year = st.number_input("출생년도", 2000, 2025, 2010)
    month = st.number_input("월", 1, 12, 6)
    day = st.number_input("일", 1, 31, 15)
    name = st.text_input("이름")

    submit = st.form_submit_button("분석")

if submit:
    일주 = 천간[(day)%10] + 지지[(day)%12]
    일간 = 일주[0]

    st.success(f"{name} 학생 분석 결과")

    # 공부 타입
    st.subheader("🧠 공부 타입")
    st.info(공부_타입(일간))

    # 풀이
    st.subheader("🔍 학습 능력 풀이")
    analysis = 공부_풀이(일간)
    st.write(f"핵심: {analysis['core']}")
    st.write(f"특징: {analysis['study']}")
    st.write(f"적용: {analysis['real']}")

    # 공부운
    st.subheader("📊 오늘 컨디션")
    집중 = random.randint(60,95)
    암기 = random.randint(50,90)

    st.metric("집중력", f"{집중}%")
    st.metric("암기력", f"{암기}%")
    st.progress(집중)

    # 전략
    st.subheader("📈 성적 상승 전략")
    st.success(성적_상승_전략(일간))

    # 약점
    st.subheader("⚠️ 약점")
    st.error(약점_분석(일간))

    # 부모
    st.subheader("👨‍👩‍👧 부모 코칭")
    for c in 부모_코칭(일간):
        st.write(f"👉 {c}")

    # 한줄 전략
    전략 = random.choice([
        "복습 중심 학습",
        "문제풀이 집중",
        "암기 과목 공략"
    ])
    st.info(f"👉 오늘 전략: {전략}")

    # PDF
    text = f"""
    유형: {공부_타입(일간)}
    전략: {성적_상승_전략(일간)}
    약점: {약점_분석(일간)}
    """

    pdf = create_pdf(name, text)

    st.download_button(
        label="📄 PDF 다운로드",
        data=pdf,
        file_name=f"{name}_리포트.pdf",
        mime="application/pdf"
    )