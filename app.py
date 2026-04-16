import streamlit as st
from datetime import datetime
import random

천간 = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
지지 = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

오행 = {"갑":"목","을":"목","병":"화","정":"화","무":"토","기":"토",
        "경":"금","신":"금","임":"수","계":"수"}

yang_stems = ["갑", "병", "무", "경", "임"]

지지_오행 = {"자":"수", "축":"토", "인":"목", "묘":"목", "진":"토", "사":"화",
             "오":"화", "미":"토", "신":"금", "유":"금", "술":"토", "해":"수"}

지지_음양 = {"자":"양", "축":"음", "인":"양", "묘":"음", "진":"양", "사":"음",
             "오":"양", "미":"음", "신":"양", "유":"음", "술":"양", "해":"음"}

일간_성격 = {
    "갑": "리더십 강하고 창의적인 나무 같은 사람.", "을": "유연하고 부드러운 풀 같은 사람.",
    "병": "밝고 열정적인 불 같은 사람.", "정": "세심하고 따뜻한 불꽃 같은 사람.",
    "무": "안정적이고 든든한 산 같은 사람.", "기": "부드럽고 포용력 있는 땅 같은 사람.",
    "경": "날카롭고 정의로운 칼 같은 사람.", "신": "유연하고 예리한 보석 같은 사람.",
    "임": "넓고 흐르는 바다 같은 사람.", "계": "깊고 신비로운 물방울 같은 사람."
}

def get_sibsin(ilgan, target, is_ji=False):
    if not target: return "알 수 없음"
    il_elem = 오행.get(ilgan, "")
    if is_ji:
        tg_elem = 지지_오행.get(target, "")
        tg_polarity = 지지_음양.get(target, "양")
    else:
        tg_elem = 오행.get(target, "")
        tg_polarity = "양" if target in yang_stems else "음"

    same_polarity = (ilgan in yang_stems) == (tg_polarity == "양")

    if il_elem == tg_elem:
        return "비견" if same_polarity else "겁재"
    elif (tg_elem == "수" and il_elem == "목") or (tg_elem == "목" and il_elem == "화") or          (tg_elem == "화" and il_elem == "토") or (tg_elem == "토" and il_elem == "금") or          (tg_elem == "금" and il_elem == "수"):
        return "정인" if same_polarity else "편인"
    elif (il_elem == "수" and tg_elem == "목") or (il_elem == "목" and tg_elem == "화") or          (il_elem == "화" and tg_elem == "토") or (il_elem == "토" and tg_elem == "금") or          (il_elem == "금" and tg_elem == "수"):
        return "식신" if same_polarity else "상관"
    elif (il_elem == "목" and tg_elem == "토") or (il_elem == "화" and tg_elem == "금") or          (il_elem == "토" and tg_elem == "수") or (il_elem == "금" and tg_elem == "목") or          (il_elem == "수" and tg_elem == "화"):
        return "정재" if same_polarity else "편재"
    else:
        return "정관" if same_polarity else "편관"

def is_current_daewoon(daewoon_str, current_age):
    age_range = daewoon_str.split(" : ")[0]
    start = int(age_range.split("세")[0])
    end = int(age_range.split("~")[1].replace("세","").strip())
    return start <= current_age <= end

def 종합운_해석(ilgan, ganji):
    stem, branch = ganji[0], ganji[1]
    stem_sib = get_sibsin(ilgan, stem)
    branch_sib = get_sibsin(ilgan, branch, True)

    jae_level = "강함" if "재" in (stem_sib + branch_sib) else "약함"
    gwan_level = "강함" if "관" in (stem_sib + branch_sib) else "약함"
    business_level = "강함" if "식" in (stem_sib + branch_sib) or "상관" in (stem_sib + branch_sib) else "약함"

    if gwan_level == "강함" and business_level == "약함":
        type_name = "직장 안정형"
    elif gwan_level == "약함" and business_level == "강함":
        type_name = "사업형"
    else:
        type_name = "하이브리드형"

    return {
        "type": type_name,
        "jae_level": jae_level,
        "gwan_level": gwan_level,
        "business_level": business_level
    }

def 한줄_요약(result):
    return f"{result['type']} | 💰{result['jae_level']} 💼{result['gwan_level']} 🚀{result['business_level']}"

st.set_page_config(page_title="🔮 사주 앱", layout="centered")

st.title("🔮 사주팔자 종합 운세")

with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("년도", 1900, 2100, 1990)
        month = st.number_input("월", 1, 12, 6)
        day = st.number_input("일", 1, 31, 15)
    with col2:
        hour = st.selectbox("시간", ["모름"] + [f"{i:02d}" for i in range(24)])
        gender = st.selectbox("성별", ["남성", "여성"])

    submit = st.form_submit_button("운세 보기")

if submit:
    hour_num = 12 if hour == "모름" else int(hour)

    년주 = 천간[(year-4)%10] + 지지[(year-4)%12]
    월주 = 천간[(month)%10] + 지지[(month)%12]
    일주 = 천간[(day)%10] + 지지[(day)%12]

    일간 = 일주[0]

    current_year = datetime.now().year
    current_age = current_year - year

    st.success(f"현재 나이: {current_age}세")

    st.write(f"년주: {년주} / 월주: {월주} / 일주: {일주}")

    st.info(f"성격: {일간_성격.get(일간)}")

    대운들 = [f"{i*10}세 ~ {i*10+9}세 : {천간[i%10]}{지지[i%12]}" for i in range(1,9)]

    st.subheader("📊 대운 분석")

    for 대운 in 대운들:
        ganji = 대운.split(" : ")[1]
        result = 종합운_해석(일간, ganji)

        is_current = is_current_daewoon(대운, current_age)

        if is_current:
            st.markdown(f"### 🔥 현재 대운: {대운}")
            st.progress(100)
        else:
            st.markdown(f"{대운}")

        st.success(한줄_요약(result))

        score_map = {"약함":30, "강함":90}
        st.progress(score_map[result["jae_level"]])

    st.info(random.choice([
        "지금은 기회를 잡아야 할 시기입니다.",
        "안정보다 도전이 유리합니다.",
        "인맥이 돈으로 연결됩니다.",
        "무리한 확장은 금물입니다."
    ]))
