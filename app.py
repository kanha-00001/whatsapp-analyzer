import streamlit as st
from preprocessor import preprocess 


st.sidebar.title("whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode("utf-8")

    df= preprocess(data)
    st.dataframe(df)

    users_list =df["user"].unique().tolist()

    users_list.sort()
    users_list.insert(0,"select the user")
    st.sidebar.selectbox("show analysis wrt USER_LIST",users_list)

    