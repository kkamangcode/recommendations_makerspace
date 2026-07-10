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


def calculate_recommendation_score(place, region, reserve, university):
    score = 0
    reasons = []

    if place["지역"] == region:
        score += 3
        reasons.append("희망 지역과 일치")

    if place["예약 가능 여부"] == reserve:
        score += 2
        reasons.append("예약 가능 조건과 일치")

    if place["대학교 내 여부"] == university:
        score += 1
        reasons.append("대학교 내 여부 조건과 일치")

    return score, reasons


def get_smart_recommendations(places, region, reserve, university, top_n=3):
    if top_n < 1:
        raise ValueError("top_n은 1 이상이어야 합니다.")

    required_keys = {
        "이름", "지역", "대학교 내 여부",
        "예약 가능 여부", "예약 사이트", "전화번호"
    }
    result = []

    for original_place in places:
        missing_keys = required_keys - set(original_place.keys())

        if missing_keys:
            missing_text = ", ".join(sorted(missing_keys))
            raise ValueError(f"필수 정보가 없습니다: {missing_text}")

        place = original_place.copy()
        score, reasons = calculate_recommendation_score(
            place, region, reserve, university
        )

        place["추천 점수"] = score
        if reasons:
            place["추천 이유"] = ", ".join(reasons)
        else:
            place["추천 이유"] = "선택한 조건과 일치하는 항목이 적음"

        result.append(place)

    result.sort(key=lambda item: (-item["추천 점수"], item["이름"]))
    return result[:top_n]


def show_smart_recommendations(recommendations):
    st.subheader("맞춤 추천 결과")

    if len(recommendations) == 0:
        st.warning("추천할 장소가 없습니다.")
        return

    for rank, place in enumerate(recommendations, start=1):
        st.markdown(f"### {rank}위. {place['이름']}")
        st.write("추천 점수:", f"{place['추천 점수']}점 / 6점")
        st.write("추천 이유:", place["추천 이유"])
        st.write("지역:", place["지역"])
        st.write("대학교 내 여부:", place["대학교 내 여부"])
        st.write("예약 가능 여부:", place["예약 가능 여부"])
        st.write("예약 사이트:", place["예약 사이트"])
        st.write("전화번호:", place["전화번호"])
        st.write("---")


def smart_recommendation_menu():
    st.subheader("사용자 맞춤 추천")
    st.caption("지역 3점, 예약 가능 여부 2점, 대학교 내 여부 1점")

    regions = sorted({place["지역"] for place in st.session_state.places})

    selected_region = st.selectbox(
        "희망 지역을 선택하세요",
        regions,
        key="smart_region"
    )
    selected_reserve = st.radio(
        "예약 가능 여부",
        ["O", "X"],
        key="smart_reserve"
    )
    selected_university = st.radio(
        "대학교 내 장소 여부",
        ["O", "X"],
        key="smart_university"
    )

    max_count = len(st.session_state.places)
    top_n = st.slider(
        "추천받을 장소 수",
        min_value=1,
        max_value=max_count,
        value=min(3, max_count)
    )

    if st.button("맞춤 추천 받기"):
        recommendations = get_smart_recommendations(
            st.session_state.places,
            selected_region,
            selected_reserve,
            selected_university,
            top_n
        )
        show_smart_recommendations(recommendations)


init_places()

st.title("강원 청소년 생활 도우미")

menu = st.sidebar.radio(
    "메뉴를 선택하세요",
    ["전체 장소 보기", "조건 검색", "맞춤 추천", "지역별 그래프", "장소 추가"]
)

if menu == "전체 장소 보기":
    show_all(st.session_state.places)

elif menu == "조건 검색":
    search_menu()

elif menu == "맞춤 추천":
    smart_recommendation_menu()

elif menu == "지역별 그래프":
    show_region_graph(st.session_state.places)

elif menu == "장소 추가":
    add_place()
