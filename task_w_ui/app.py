import streamlit as st
import time
from PIL import Image
from functions import *

st.set_page_config(layout="wide")

st.title("Face Checker!")


# sidebar components
st.sidebar.title("Enter Folder Directory")
path = st.sidebar.text_input("Path:", value="D:/DS/DS task/face-recognition/photos")


@st.cache
def hello():
    print("hello")


if "df" not in st.session_state:
    st.info("Submit photos path to continue")

if st.sidebar.button("Submit"):
    if "df" in st.session_state:
        del st.session_state["df"]
    with st.spinner("Please wait, Processing...."):
        a = all_paths(path)
        df = create_dataframe(a)
        st.session_state["df"] = df

if "df" in st.session_state:
    df = st.session_state["df"]
    st.dataframe(df)
    a = df.set_index("Name").to_dict(orient="index")
    options = st.multiselect("Select a person", list(df["Name"]))
    for name in options:
        st.subheader(name)
        img_adhaar = a[name]["Adhaar"]
        img_driver = a[name]["Drivers"]
        col1, col2 = st.columns(2)
        if img_adhaar:
            col1.write("Adhaar Image:")
            col1.image(face(img_adhaar).resize((100, 100)))
        else:
            col1.write("Adhaar Image:")
            col1.write("No Adhaar image found")
        if img_driver:
            col2.write("Drivers License Image:")
            img = face(img_driver).resize((100, 100))
            col2.image(img)
        else:
            col2.write("Drivers License Image:")
            col2.write("No Drivers License image found")
        st.markdown("""---""")
