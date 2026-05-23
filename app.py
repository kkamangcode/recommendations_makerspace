import streamlit as st


def init_places():
    if "places" not in st.session_state:
        st.session_state.places = [
            {"이름": "강원 메이커스페이스", "지역": "춘천", "대학교 내 여부": "X", "예약 가능 여부": "O", "예약 사이트": "stbc.or.kr", "전화번호": "033-245-6560"},
            {"이름": "G-MAKER LAB", "지역": "양양", "대학교 내 여부": "O", "예약 가능 여부": "O", "예약 사이트": "전화상담만 가능", "전화번호": "033-660-8262,033-660-8266"},
            {"이름": "KNU 메이커스페이스", "지역": "춘천", "대학교 내 여부": "O", "예약 가능 여부": "O", "예약 사이트": "knumakerspace.com", "전화번호": "033-250-7314"},
            {"이름": "강릉제작소", "지역": "강릉", "대학교 내 여부": "X", "예약 가능 여부": "O", "예약 사이트": "www.gnmakerspace.com", "전화번호": "033-650-3362"},
            {"이름": "JOY&DIY 메이커스페이스", "지역": "원주", "대학교 내 여부": "O", "예약 가능 여부": "O", "예약 사이트": "https://maker.halla.ac.kr/main/index.php", "전화번호": "033-760-1364"},
            {"이름": "고성 메이커스페이스", "지역": "고성", "대학교 내 여부": "X", "예약 가능 여부": "X", "예약 사이트": "직접방문", "전화번호": "033-123-4567"}
        ]


def add_place():
    st.subheader("장소 추가")

    name = st.text_input("이름")
    region = st.text_input("지역")
    univer = st.radio("대학교 내 여부", ["O", "X"], key="univer")
    reserve = st.radio("예약 가능 여부", ["O", "X"], key="reserve")
    site = st.text_input("예약 사이트")
    phone = st.text_input("전화번호")

    if st.button("장소 추가"):
        if name == "" or region == "" or site == "" or phone == "":
            st.warning("모든 정보를 입력해주세요.")
        else:
            new_place = {
                "이름": name,
                "지역": region,
                "대학교 내 여부": univer,
                "예약 가능 여부": reserve,
                "예약 사이트": site,
                "전화번호": phone
            }

            st.session_state.places.append(new_place)
            st.success("장소가 추가되었습니다.")


def show_place_detail(place):
    st.write("장소 이름은", place["이름"], "입니다")
    st.write("지역은", place["지역"], "입니다")
    st.write("대학교 내 여부는", place["대학교 내 여부"], "입니다")
    st.write("예약 가능 여부는", place["예약 가능 여부"], "입니다")
    st.write("예약 사이트는", place["예약 사이트"], "입니다")
    st.write("전화번호는", place["전화번호"], "입니다")
    st.write("---")


def show_all(places):
    st.subheader("전체 장소 보기")

    for place in places:
        show_place_detail(place)


def get_recommendations(places, region, reserve):
    result = []

    for place in places:
        if place["지역"] == region and place["예약 가능 여부"] == reserve:
            result.append(place)

    return result


def show_recommendations(recommendations):
    st.subheader("추천 장소 보기")

    if len(recommendations) == 0:
        st.write("조건에 맞는 장소가 없습니다.")
    else:
        for place in recommendations:
            st.write("추천장소는", place["이름"], "입니다")
            st.write("예약 사이트는", place["예약 사이트"], "입니다")
            st.write("전화번호는", place["전화번호"], "입니다")
            st.write("---")


def show_region_graph(places):
    region_count = {}

    for place in places:
        region = place["지역"]

        if region not in region_count:
            region_count[region] = 1
        else:
            region_count[region] += 1

    st.subheader("지역별 장소 개수 그래프")
    st.bar_chart(region_count)


def search_menu():
    st.subheader("조건 검색")

    selected_region = st.selectbox(
        "지역을 선택하세요",
        ["강릉", "춘천", "양양", "원주", "고성"]
    )

    selected_reserve = st.radio(
        "예약 가능 여부를 선택하세요",
        ["O", "X"],
        key="selected_reserve"
    )

    if st.button("추천 보기"):
        recommendations = get_recommendations(
            st.session_state.places,
            selected_region,
            selected_reserve
        )
        show_recommendations(recommendations)


init_places()

st.title("강원 청소년 생활 도우미")

menu = st.sidebar.radio(
    "메뉴를 선택하세요",
    ["전체 장소 보기", "조건 검색", "지역별 그래프", "장소 추가"]
)

if menu == "전체 장소 보기":
    show_all(st.session_state.places)

elif menu == "조건 검색":
    search_menu()

elif menu == "지역별 그래프":
    show_region_graph(st.session_state.places)

elif menu == "장소 추가":
    add_place()
