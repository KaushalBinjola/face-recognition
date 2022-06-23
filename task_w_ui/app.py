import streamlit as st
import time
from functions import *

st.title("Face Checker!")

a = None
# sidebar components
st.sidebar.title("Enter Folder Directory")
path = st.sidebar.text_input("Path:", value="D:/DS/DS task/photos")
if st.sidebar.button("Submit"):
    with st.spinner("Please wait, Processing...."):
        a = all_paths(path)
        # st.write(a)
        df = create_dataframe(a)
        st.dataframe(df)


@st.cache
def hello():
    print("hello")


# ankeetpujara@gmail.com
