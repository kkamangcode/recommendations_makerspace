import streamlit as st
import pandas as pd

st.title("강원생활도우미 2.0")
st.write("엑셀 화일을 업로드 할 수 있습니다")

upload_file = st.file_uploader(
  "장소 데이터 엑셀 파일을  업로드해주세요.",
  type=["xlsx"]
)

if upload_file is not None:
  df = pd.read_excel(upload_file)
  st.subheader("업로드한 장소 목록")
  st.dataframe(df)
else:
  st.info("데이터를 저장한 엑셀(확장자.xlsx)화일을 업로드하세요")
