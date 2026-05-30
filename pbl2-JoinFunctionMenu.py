import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    # 숫자형 데이터 정리
    if "예산" in merged_df.columns:
        merged_df["예산"] = pd.to_numeric(merged_df["예산"], errors="coerce").fillna(0)

    if "평점" in merged_df.columns:
        merged_df["평점"] = pd.to_numeric(merged_df["평점"], errors="coerce").fillna(0)

    return merged_df


def get_options(df, column):
    return ["전체"] + sorted(df[column].dropna().unique().tolist())


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)


def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox("지역 선택", get_options(df, "지역"))
    selected_type = st.selectbox("유형 선택", get_options(df, "유형"))

    selected_purpose = st.selectbox("추천목적 선택", get_options(df, "추천목적"))
    selected_situation = st.selectbox("추천상황 선택", get_options(df, "추천상황"))
    selected_target = st.selectbox("추천대상 선택", get_options(df, "추천대상"))

    selected_indoor = st.selectbox("실내여부 선택", get_options(df, "실내여부"))
    selected_time = st.selectbox("소요시간 선택", get_options(df, "소요시간"))
    selected_reservation = st.selectbox("예약필요/여부 선택", get_options(df, "예약필요"))

    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    selected_rating = st.slider(
        "최소 평점",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )

    result = df.copy()

    if selected_region != "전체":
        result = result[result["지역"] == selected_region]

    if selected_type != "전체":
        result = result[result["유형"] == selected_type]

    if selected_purpose != "전체":
        result = result[result["추천목적"] == selected_purpose]

    if selected_situation != "전체":
        result = result[result["추천상황"] == selected_situation]

    if selected_target != "전체":
        result = result[result["추천대상"] == selected_target]

    if selected_indoor != "전체":
        result = result[result["실내여부"] == selected_indoor]

    if selected_time != "전체":
        result = result[result["소요시간"] == selected_time]

    if selected_reservation != "전체":
        result = result[result["예약필요"] == selected_reservation]

    result = result[
        (result["예산"] <= selected_budget) &
        (result["평점"] >= selected_rating)
    ]

    result = result.sort_values(
        by=["평점", "예산"],
        ascending=[False, True]
    )

    st.subheader("검색 결과")

    if len(result) > 0:
        st.write(f"총 {len(result)}개의 추천 장소가 있습니다.")
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        [
            "지역",
            "유형",
            "실내여부",
            "추천목적",
            "추천상황",
            "추천대상",
            "소요시간",
            "예약필요"
        ]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)

else:
    st.info("엑셀 파일을 업로드하면 앱을 사용할 수 있습니다.")
