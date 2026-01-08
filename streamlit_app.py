import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time

# 앱의 제목
st.title("🎈 Streamlit Elements — 한 페이지 데모")

# 간단한 설명 텍스트
st.markdown("""
이 페이지는 Streamlit에서 단일 페이지에 넣을 수 있는 주요 요소들을 **예시와 함께** 보여줍니다.
각 섹션 위에 한국어 각주(주석)를 달아 공부하기 쉽게 만들었습니다.
""")

# --------------------------------------------------
# 텍스트 관련
# --------------------------------------------------
st.header("텍스트 요소들")
# st.write는 다양한 타입(문자열, 숫자, HTML 등)을 자동으로 렌더링합니다.
st.write("st.write: 일반 텍스트와 객체를 렌더링합니다.")
st.markdown("st.markdown: Markdown 문법을 사용하여 서식을 적용합니다. **굵게**, *기울임* 등.")
st.caption("st.caption: 보조 설명(작은 글씨)")
st.subheader("subheader: 작은 제목")
st.code("print('Hello Streamlit')")  # 코드 블록 예시

# Latex 수식
st.latex(r"E = mc^2")

# --------------------------------------------------
# 기본 위젯들
# --------------------------------------------------
st.header("입력 위젯들")

st.write("버튼, 체크박스, 라디오, 셀렉트박스, 멀티셀렉트 등")

if st.button("클릭 버튼 (st.button)"):
    st.success("버튼을 클릭했습니다!")

agree = st.checkbox("체크박스 (st.checkbox)")
st.write("체크 여부:", agree)

choice = st.radio("라디오 선택 (st.radio)", ("옵션 A", "옵션 B", "옵션 C"))
st.write("선택:", choice)

sel = st.selectbox("셀렉트박스 (st.selectbox)", ["사과", "바나나", "체리"])  # 단일 선택
st.write("선택된 과일:", sel)

multi = st.multiselect("멀티셀렉트 (st.multiselect)", ["파이썬","자바스크립트","러스트"], default=["파이썬"])  # 다중 선택
st.write("관심있는 언어:", multi)

# 숫자/텍스트 입력
num = st.number_input("숫자 입력 (st.number_input)", min_value=0, max_value=100, value=10)
st.write("입력된 숫자:", num)

text = st.text_input("텍스트 입력 (st.text_input)", value="안녕하세요")
st.write("입력된 텍스트:", text)

password = st.text_input("비밀번호(보이기/숨기기)", type="password")
# 날짜/시간
dt = st.date_input("날짜 선택 (st.date_input)", value=date.today())
st.write("선택된 날짜:", dt)
tm = st.time_input("시간 선택 (st.time_input)", value=time(12, 30))
st.write("선택된 시간:", tm)

# 파일 업로드
uploaded = st.file_uploader("파일 업로드 (st.file_uploader)")
if uploaded:
    st.write("업로드된 파일 이름:", uploaded.name)

# --------------------------------------------------
# 레이아웃: 컬럼/탭/폼
# --------------------------------------------------
st.header("레이아웃 & 컨테이너")

col1, col2 = st.columns(2)
with col1:
    st.metric("온도", "21°C", delta="+1.2°C")  # 지표 위젯
with col2:
    st.metric("습도", "60%", delta="-2%")

tabs = st.tabs(["Tab A", "Tab B"])
with tabs[0]:
    st.write("첫 번째 탭 내용")
with tabs[1]:
    st.write("두 번째 탭 내용")

with st.expander("폼 예시 (st.form)"):
    with st.form("my_form"):
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=0, max_value=120)
        submitted = st.form_submit_button("제출")
        if submitted:
            st.write(f"{name}님, 나이 {age} 등록 완료")

# --------------------------------------------------
# 미디어: 이미지/오디오/비디오
# --------------------------------------------------
st.header("미디어")
st.write("이미지, 오디오, 비디오를 렌더링합니다.")
st.image(
    "https://docs.streamlit.io/images/brand/streamlit-mark-color.png",
    width=120,
)

# 간단한 오디오/비디오(외부 URL 혹은 바이너리 데이터)
# st.audio(...), st.video(...)

# --------------------------------------------------
# 데이터 표시: dataframe, table
# --------------------------------------------------
st.header("데이터 시각화 & 표")
df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])  # 예시 데이터프레임
st.dataframe(df)  # 대화형 표
st.table(df.head())  # 정적 표

# 차트: 라인/바/영역 차트 (내장)
st.line_chart(df)
st.bar_chart(df)

# 지도: 간단한 lat/lon 표시
map_df = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.55, 126.97], columns=["lat", "lon"]
)
st.map(map_df)

# --------------------------------------------------
# 진행 상태/대기 UI
# --------------------------------------------------
st.header("상태표시 및 애니메이션")
with st.spinner("처리 중..."):
    # 실제로는 시간이 걸리는 작업을 여기에 둡니다.
    pass

progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

st.balloons()

# --------------------------------------------------
# 고급: 플로팅 HTML, 플롯 라이브러리 연동 예시
# --------------------------------------------------
st.header("고급 위젯 및 외부 라이브러리 연동")
st.write("Plotly, Altair, Matplotlib 등과 쉽게 연동됩니다.")

import altair as alt
chart = alt.Chart(df.reset_index()).mark_line().encode(x="index", y="a")
st.altair_chart(chart, use_container_width=True)

# --------------------------------------------------
# 학습용 팁 (각주 형식)
# --------------------------------------------------
st.markdown("""
**학습 팁:**
- 각 `st.` 함수는 화면에 UI를 추가합니다. 함수 호출 순서가 위에서 아래로 렌더링 순서가 됩니다.
- 위젯(입력)은 상태(state)를 가지므로 사용자의 상호작용에 따라 재실행(re-run)됩니다.
- 복잡한 레이아웃은 `columns`, `tabs`, `container`, `expander` 등을 조합해 만듭니다.
- 외부 라이브러리로 만든 Figure 객체는 `st.pyplot`, `st.plotly_chart`, `st.altair_chart` 등으로 표시합니다.
""")

st.info("이 페이지의 코드를 읽고, 각 섹션을 차례로 실행해 보세요.")

# 끝
