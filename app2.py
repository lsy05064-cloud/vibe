import streamlit as st
import re
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
from io import BytesIO

def classify_bmi(bmi: float) -> tuple[str, str, str]:
    """대한비만학회(아시아-태평양) 기준 BMI 분류
    반환: (분류명, 이모지, 건강정보 안내문)
    """
    if bmi < 18.5:
        return ("저체중", "🟦",
                "체중이 표준보다 적은 상태입니다. 단백질과 탄수화물을 골고루 갖춘 "
                "규칙적인 식사를 하고, 근육량을 늘리는 가벼운 근력 운동을 권장합니다. "
                "급격한 체중 감소가 있었다면 병원 진료를 받아보세요.")
    elif bmi < 23:
        return ("정상", "🟩",
                "건강한 체중 범위입니다. 지금의 식습관과 활동량을 잘 유지하세요. "
                "주 3회 이상, 30분 이상의 유산소 운동을 꾸준히 하면 "
                "현재의 건강 상태를 오래 지킬 수 있습니다.")
    elif bmi < 25:
        return ("과체중", "🟨",
                "정상 범위를 조금 넘어선 상태입니다. 야식과 당분 섭취를 줄이고, "
                "걷기·자전거 같은 유산소 운동을 주 4회 이상 실천해 보세요. "
                "지금 관리하면 비만으로의 진행을 충분히 막을 수 있습니다.")
    elif bmi < 30:
        return ("비만 1단계", "🟧",
                "체중 조절이 필요한 단계입니다. 식사량을 조금 줄이고 "
                "규칙적인 운동을 병행하면 개선할 수 있습니다. 고혈압, 당뇨 등 "
                "동반 질환 여부를 확인하기 위해 건강검진을 권장합니다.")
    else:
        return ("비만 2단계 이상", "🟥",
                "적극적인 체중 관리가 필요한 단계입니다. 혼자 하기보다는 "
                "의사, 영양사 등 전문가와 상담하여 체계적인 계획을 세우는 것이 "
                "안전하고 효과적입니다. 가까운 병원이나 보건소를 방문해 보세요.")

def speak(text: str) -> BytesIO:
    """텍스트를 한국어 음성(mp3 바이트)으로 변환"""
    tts = gTTS(text=text, lang="ko")
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf

text = "마이크 버튼을 누르고 키와 몸무게를 말하면, BMI와 건강정보를 음성으로 알려드립니다."
if st.button("🎵 음성 BMI 건강 도우미 클릭"):
    audio = speak(text)
    st.audio(audio, format="audio/mp3", autoplay=True)

# if st.button("🎵 음성 BMI 건강 도우미"):
#     tts = gTTS(text=text, lang='ko')     # 한국어 설정
#     audio_bytes = BytesIO()               # 파일 저장 없이 메모리에서 처리
#     tts.write_to_fp(audio_bytes)
#     audio_bytes.seek(0)
#     st.audio(audio_bytes, format='audio/mp3')   # 재생 플레이어 표시


st.write("마이크 버튼을 누르고 키를 숫자를 말해보세요. 예: '삼십오' 또는 '35'")

# 1단계: 음성 → 텍스트 (한국어 설정: language='ko')
height_text = speech_to_text(
    language='ko',              # 한국어 인식
    start_prompt="🎙️ 녹음 시작",
    stop_prompt="⏹️ 녹음 종료",
    just_once=True,             # 한 번 인식 후 초기화
    use_container_width=True,
    key='stt1'
)

# 2단계: 텍스트 → 숫자 추출
if height_text:
    st.info(f"인식된 말: **{height_text}**")
    numbers = re.findall(r'\d+\.?\d*', height_text)   # 아라비아 숫자 추출
    if numbers:
        height_value = float(numbers[0])
        st.success(f"✅ 입력된 숫자: **{height_value}**")
        st.session_state.height = height_value
        #st.session_state['voice_number'] = height_value
    else:
        st.warning("⚠️ 숫자를 찾지 못했어요. '35'처럼 또박또박 말해보세요.")

# 3단계: 입력받은 숫자를 위젯에 반영
# default = st.session_state.get('voice_number', 0.0)
# num = st.number_input("확인/수정", value=default)

st.write("마이크 버튼을 누르고 몸무게를 숫자를 말해보세요. 예: '칠십오' 또는 '75'")

# 1단계: 음성 → 텍스트 (한국어 설정: language='ko')
weight_text = speech_to_text(
    language='ko',              # 한국어 인식
    start_prompt="🎙️ 녹음 시작",
    stop_prompt="⏹️ 녹음 종료",
    just_once=True,             # 한 번 인식 후 초기화
    use_container_width=True,
    key='stt2'
)

# 2단계: 텍스트 → 숫자 추출
if weight_text:
    st.info(f"인식된 말: **{weight_text}**")
    numbers = re.findall(r'\d+\.?\d*', weight_text)   # 아라비아 숫자 추출
    if numbers:
        weight_value = float(numbers[0])
        st.success(f"✅ 입력된 숫자: **{weight_value}**")
        st.session_state.weight = weight_value
        #st.session_state['voice_number'] = weight_value
    else:
        st.warning("⚠️ 숫자를 찾지 못했어요. '75'처럼 또박또박 말해보세요.")


if st.button("🧮 BMI 계산하고 음성으로 듣기", use_container_width=True, type="primary"):
    height = st.number_input(
        "키 (cm)", min_value=0.0, max_value=250.0,
        value=float(st.session_state.height or 0.0), step=0.1,
    )
    weight = st.number_input(
        "몸무게 (kg)", min_value=0.0, max_value=300.0,
        value=float(st.session_state.weight or 0.0), step=0.1
    )

    if height <= 0 or weight <= 0:
        st.warning("⚠️ 키와 몸무게를 먼저 입력해 주세요.")
    else:
        bmi = weight / ((height / 100) ** 2)
        category, emoji, advice = classify_bmi(bmi)
 
        # 화면 표시
        st.metric(label="당신의 BMI", value=f"{bmi:.1f}", delta=category)
        st.markdown(f"### {emoji} 판정: **{category}**")
        st.info(advice)


        message = (
            f"측정 결과를 알려드립니다. 키 {height:.0f} 센티미터, "
            f"몸무게 {weight:.0f} 킬로그램으로, "
            f"비엠아이 수치는 {bmi:.1f} 입니다. {category}에 해당합니다. {advice}"
        )
        with st.spinner("음성을 생성하는 중..."):
            audio = speak(message)
        st.audio(audio, format="audio/mp3")
        st.caption("▶️ 재생 버튼을 눌러 결과를 들어보세요.")
