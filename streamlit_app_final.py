import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="후원 타임스탬프 기록기", layout="centered")
st.title("🎬 후원 타임스탬프 기록기 (Streamlit)")

# 입력창: 방송 시작 시간
start_str = st.text_input("방송 시작 시간 (YYYY-MM-DD HH:mm:ss)", "")

# 세션 상태 초기화
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["TimeStamp", "닉네임", "개수", "시그니처 이름", "1+1"])
if "clicked_time" not in st.session_state:
    st.session_state["clicked_time"] = None

# 시작 시간 설정
if st.button("✅ 시작 시간 설정"):
    try:
        st.session_state["start_time"] = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        st.success(f"시작 시간 설정 완료: {st.session_state['start_time']}")
    except:
        st.error("형식이 올바르지 않습니다. 예: 2025-06-01 22:30:00")

# 타임스탬프 버튼 클릭 → 현재 시간 저장
if st.button("⏱ Time Stamp 추가"):
    if st.session_state["start_time"]:
        st.session_state["clicked_time"] = datetime.now()
    else:
        st.warning("먼저 방송 시작 시간을 설정하세요.")

# 클릭 시간 → 타임스탬프 계산하여 새로운 행 추가
if st.session_state["clicked_time"]:
    diff = st.session_state["clicked_time"] - st.session_state["start_time"]

    # 음수 시간은 00:00:00 처리
    if diff.total_seconds() < 0:
        diff = timedelta(seconds=0)

    ts = str(diff).split('.')[0]
    if len(ts.split(":")) == 2:
        ts = "00:" + ts

    new_row = pd.DataFrame([{
        "TimeStamp": ts,
        "닉네임": "",
        "개수": "",
        "시그니처 이름": "",
        "1+1": False
    }])
    st.session_state["data"] = pd.concat([st.session_state["data"], new_row], ignore_index=True)
    st.session_state["clicked_time"] = None

# 편집 가능한 테이블 표시
edited_df = st.data_editor(
    st.session_state["data"],
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "1+1": st.column_config.CheckboxColumn("1+1 여부")
    }
)
st.session_state["data"] = edited_df

# 저장 및 다운로드 버튼
if st.button("💾 저장 및 다운로드"):
    today = datetime.today().strftime("%y.%m.%d")
    filename = f"{today}_타임라인(플단리스트)(TimeStamp).txt"

    with open(filename, "w", encoding="utf-8") as f:
        for _, row in st.session_state["data"].iterrows():
            if row["TimeStamp"]:
                line = f"{row['TimeStamp']} {row['닉네임']}\t\t{row['개수']} {row['시그니처 이름']}"
                if row["1+1"]:
                    line += " 1+1"
                f.write(line.strip() + "\n")

    with open(filename, "rb") as f:
        st.download_button("📥 타임라인 파일 다운로드", f, file_name=filename, mime="text/plain")

