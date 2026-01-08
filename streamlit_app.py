import streamlit as st
from PIL import Image
import io

# -------------------------------------------
# 초등학교 곱셈 학습 웹 앱
# 기능:
# 1) 사용자가 두 숫자(행 x 열)를 입력하고 그림(또는 업로드 이미지)을 선택
# 2) 선택된 그림으로 곱셈 결과를 시각화(격자 형태로 표시)
# 3) 시각화 완료 후 계산 결과값을 입력하는 칸이 나타남
# 4) 정답 여부를 표시
# 5) 초기화 버튼으로 상태를 리셋
# 모든 섹션에 학습용 설명(한국어 각주)을 추가했습니다.
# -------------------------------------------

st.set_page_config(page_title="초등 곱셈 놀이", page_icon="🔢", layout="centered")

st.title("🔢 초등 곱셈 학습 — 그림으로 배우는 곱셈")

st.markdown("""
이 앱은 곱셈을 시각적으로 이해하도록 도와줍니다.
1) 행(세로)과 열(가로)을 정하고
2) 그림을 골라 `시각화` 버튼을 누르면 격자로 그림이 채워집니다.
3) 그림을 보고 곱셈 결과(행 × 열)를 입력해 정답을 확인하세요.

아래 각 항목의 주석을 읽으며 코드를 공부해보세요.
""")

# 세션 상태 초기화용 기본값 설정
if "visualized" not in st.session_state:
    st.session_state.visualized = False
if "rows" not in st.session_state:
    st.session_state.rows = 3
if "cols" not in st.session_state:
    st.session_state.cols = 4
if "chosen_mode" not in st.session_state:
    st.session_state.chosen_mode = "이모지"
if "uploaded_img" not in st.session_state:
    st.session_state.uploaded_img = None
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "checked" not in st.session_state:
    st.session_state.checked = False

# ----------------------
# 입력: 행/열, 그림 선택
# ----------------------
st.subheader("1) 문제 설정")
# 숫자 입력: 행(세로)과 열(가로)을 정함
# 초등학생 학습용으로 너무 큰 숫자는 피하도록 범위 제한
rows = st.number_input("행(세로) 수", min_value=1, max_value=12, value=st.session_state.rows, key="rows_input")
cols = st.number_input("열(가로) 수", min_value=1, max_value=12, value=st.session_state.cols, key="cols_input")

# 그림 선택: 간단한 이모지 모음이나 이미지 업로드 선택
st.write("그림 선택 (미리보기 포함)")
mode = st.radio("표시 방식 선택", ("이모지", "이미지 URL(사과/별)", "업로드 이미지"), index=0, key="mode_radio")

# 몇 가지 이미지 URL 샘플 제공 (외부이미지 사용시 네트워크 필요)
sample_urls = {
    "사과": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg",
    "별": "https://upload.wikimedia.org/wikipedia/commons/1/18/Five-pointed_star.svg"
}

uploaded_file = None
chosen_emoji = "🍎"
chosen_url = None

if mode == "이모지":
    # 간단한 이모지 선택
    chosen_emoji = st.selectbox("이모지 선택", ("🍎 사과", "⭐ 별", "🐶 강아지", "🍪 쿠키"))
    # 선택된 텍스트에서 실제 이모지만 추출
    chosen_emoji = chosen_emoji.split()[0]
    st.caption("이모지는 텍스트로 렌더링되며 크기는 브라우저/OS에 따라 다릅니다.")
elif mode == "이미지 URL(사과/별)":
    # 이미지 URL 선택
    sel = st.selectbox("샘플 이미지 선택", ("사과", "별"))
    chosen_url = sample_urls[sel]
    st.image(chosen_url, width=80, caption=f"샘플: {sel}")
else:
    # 업로드된 이미지를 저장
    uploaded_file = st.file_uploader("이미지 업로드 (투명배경 권장)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # PIL로 읽어서 세션에 보관
        st.session_state.uploaded_img = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(st.session_state.uploaded_img, width=120, caption="업로드된 이미지 미리보기")

# ----------------------
# 시각화 버튼: 격자 표시
# ----------------------
st.subheader("2) 시각화")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("시각화"):
        # 입력값을 세션 상태에 저장하고 정답(행*열)을 계산
        st.session_state.rows = int(rows)
        st.session_state.cols = int(cols)
        st.session_state.chosen_mode = mode
        st.session_state.correct_answer = st.session_state.rows * st.session_state.cols
        st.session_state.visualized = True
        st.session_state.checked = False
with col2:
    # 초기화 버튼: 세션 상태를 초기값으로 되돌리고 페이지 재실행
    if st.button("초기화"):
        st.session_state.visualized = False
        st.session_state.rows = 3
        st.session_state.cols = 4
        st.session_state.chosen_mode = "이모지"
        st.session_state.uploaded_img = None
        st.session_state.correct_answer = None
        st.session_state.checked = False
        st.experimental_rerun()

# ----------------------
# 시각화 출력 영역
# ----------------------
if st.session_state.visualized:
    st.markdown(f"**{st.session_state.rows} × {st.session_state.cols} = ?**  — 아래 그림을 보고 정답을 입력하세요.")

    # 격자 형태로 그림을 출력: 행 수만큼 반복해서 각 행에 'cols'개의 열 생성
    for r in range(st.session_state.rows):
        cols_objs = st.columns(st.session_state.cols)
        for c_idx, col_obj in enumerate(cols_objs):
            if st.session_state.chosen_mode == "이모지":
                # 이모지는 텍스트로 출력
                col_obj.markdown(f"<div style='font-size:40px; text-align:center'>{chosen_emoji}</div>", unsafe_allow_html=True)
            elif st.session_state.chosen_mode == "이미지 URL(사과/별)":
                # 외부 URL 이미지 출력
                col_obj.image(chosen_url, use_column_width=True)
            else:
                # 업로드 이미지 출력
                if st.session_state.uploaded_img is not None:
                    col_obj.image(st.session_state.uploaded_img, use_column_width=True)
                else:
                    col_obj.write("(업로드된 이미지 없음)")

    # ----------------------
    # 정답 입력 및 확인
    # ----------------------
    st.subheader("3) 정답 입력")
    # 사용자의 정답 입력란 (정수만 받도록 설정)
    user_ans = st.number_input("곱셈 결과를 입력하세요", min_value=0, step=1, key="user_ans_input")
    if st.button("정답 확인"):
        st.session_state.checked = True
        if st.session_state.correct_answer is not None and int(user_ans) == st.session_state.correct_answer:
            st.success(f"정답입니다!  {st.session_state.rows} × {st.session_state.cols} = {st.session_state.correct_answer}")
        else:
            st.error(f"틀렸습니다. 다시 확인해보세요. (정답은 {st.session_state.correct_answer} 입니다)")

    # 힌트 토글: 학생용 힌트(행×열을 세어보는 방법 안내)
    with st.expander("힌트 보기"):
        st.write("그림을 가로로 몇 개, 세로로 몇 개인지 세어보세요. 예: 3행 × 4열 = 각 행에 4개씩, 총 12개")

else:
    st.info("왼쪽에서 숫자와 그림을 선택한 후 '시각화' 버튼을 눌러 시작하세요.")

# ----------------------
# 하단: 학습 팁 및 코드 주석 안내
# ----------------------
st.markdown("""
---
**코드 학습 팁 (각주):**
- `st.session_state`를 사용하면 버튼 클릭 등으로 발생한 상태를 페이지 전역에서 유지할 수 있습니다.
- `st.columns()`를 사용하면 행 내에 여러 열을 만들 수 있어 격자 레이아웃을 쉽게 구성할 수 있습니다.
- 이미지 업로드는 `st.file_uploader`로 받고, `PIL.Image`로 읽어 `st.image`에 전달합니다.
- `st.experimental_rerun()`은 상태 재설정 후 페이지를 즉시 다시 실행할 때 유용합니다.
""")
