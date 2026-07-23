import streamlit as st

st.set_page_config(page_title="My Homepage", page_icon="👋", layout="wide")

PROFILE = {
    "name": "홍길동",
    "title": "소프트웨어 개발자",
    "bio": "안녕하세요! 저는 문제를 해결하는 것을 좋아하는 개발자입니다.",
    "email": "kang@limehotip.top",
    "github": "https://github.com/yourname",
    "linkedin": "https://linkedin.com/in/yourname",
}

SKILLS = ["Python", "JavaScript", "Streamlit", "React", "SQL", "Git"]

PROJECTS = [
    {
        "name": "프로젝트 이름 1",
        "description": "이 프로젝트에 대한 간단한 설명을 적어주세요.",
        "link": "https://github.com/yourname/project1",
    },
    {
        "name": "프로젝트 이름 2",
        "description": "이 프로젝트에 대한 간단한 설명을 적어주세요.",
        "link": "https://github.com/yourname/project2",
    },
]

with st.sidebar:
    st.title("메뉴")
    page = st.radio("이동", ["소개", "스킬", "프로젝트", "연락처"], label_visibility="collapsed")

if page == "소개":
    st.image("assets/banner.png", use_container_width=True)

    col_avatar, col_intro = st.columns([1, 3])
    with col_avatar:
        st.image("assets/avatar.png", width=150)
    with col_intro:
        st.title(f"👋 {PROFILE['name']}")
        st.subheader(PROFILE["title"])
        st.write(PROFILE["bio"])

    st.divider()
    badge_cols = st.columns(3)
    for col, (img, label) in zip(
        badge_cols,
        [
            ("assets/badge_code.png", "코딩"),
            ("assets/badge_idea.png", "아이디어"),
            ("assets/badge_rocket.png", "실행력"),
        ],
    ):
        with col:
            st.image(img, width=100)
            st.caption(label)

elif page == "스킬":
    st.title("🛠️ 스킬")
    cols = st.columns(3)
    for i, skill in enumerate(SKILLS):
        with cols[i % 3]:
            st.info(skill)

elif page == "프로젝트":
    st.title("💼 프로젝트")
    for project in PROJECTS:
        with st.container(border=True):
            st.subheader(project["name"])
            st.write(project["description"])
            st.markdown(f"[바로가기]({project['link']})")

elif page == "연락처":
    st.title("📬 연락처")
    st.write(f"**Email:** {PROFILE['email']}")
    st.write(f"**GitHub:** {PROFILE['github']}")
    st.write(f"**LinkedIn:** {PROFILE['linkedin']}")
