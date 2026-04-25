import streamlit as st

places=[
    {"이름":"강원 메이커스페이스","지역":"춘천","대학교 내 여부":"X","예약 가능 여부":"O","예약 사이트":"stbc.or.kr","전화번호":"033-245-6560"},
    {"이름":"G-MAKER LAB","지역":"양양","대학교 내 여부":"O","예약 가능 여부":"O","예약 사이트":"전화상담만 가능","전화번호":"033-660-8262,033-660-8266"},
    {"이름":"KNU 메이커스페이스","지역":"춘천","대학교 내 여부":"O","예약 가능 여부":"O","예약 사이트":"knumakerspace.com","전화번호":"033-250-7314"},
    {"이름":"강릉제작소","지역":"강릉","대학교 내 여부":"X","예약 가능 여부":"O","예약 사이트":"www.gnmakerspace.com","전화번호":"033-650-3362"},
    {"이름":"JOY&DIY 메이커스페이스","지역":"원주","대학교 내 여부":"O","예약 가능 여부":"O","예약 사이트":"https://maker.halla.ac.kr/main/index.php","전화번호":"033-760-1364"}
]
def show_all(places):
    st.subheader("전체 장소 보기")
    for place in places:
        st.write("장소 이름은",place["이름"],"입니다")
        st.write("지역은",place["지역"],"입니다")
        st.write("대학교 내 여부는",place["대학교 내 여부"],"입니다")
        st.write("예약 가능 여부는",place["예약 가능 여부"],"입니다")
        st.write("예약 사이트는",place["예약 사이트"],"입니다")
        st.write("전화번호는",place["전화번호"],"입니다")
def get_recommendations(data, region, reserve):
    result = []
    for place in data:
        if place["지역"] == region and place["예약 가능 여부"] == reserve:
            result.append(place)
    return result

st.title("강원 청소년 생활 도우미")
selected_region = st.selectbox("지역을 선택하세요", ["강릉","춘천","양양","원주"])
selected_reserve = st.radio("예약 가능 여부를 선택하세요", ["O", "X"])

if st.button("추천 보기"):
    recommendations = get_recommendations(places, selected_region, selected_reserve)

    if len(recommendations) == 0:
        st.write("조건에 맞는 장소가 없습니다")
    else:
        for place in recommendations:
            st.write("추천장소는",place["이름"],"입니다")
            st.write("예약 사이트는",place["예약 사이트"],"입니다")
            st.write("전화번호는",place["전화번호"],"입니다")
            st.write("---")
