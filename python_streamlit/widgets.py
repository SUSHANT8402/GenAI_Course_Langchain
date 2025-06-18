import streamlit as st
import pandas as pd

st.title("Streamlit text input")
name=st.text_input("Enter your name")


age=st.slider("select your age",0,100,25)
st.write(f"your age is {age}")

options=["Python","Java","C++","JavaScript"]
choice=st.selectbox("choose your favourite language",options)
st.write(f"you selected {choice}")

if name:
    st.write(f"hello, {name}")
    
data={
    "Name":["John","Jane","Jake","Jill"],
    "Age":[28,45,55,60],
    "City":["New york","Los Angkes","Chicago","Huston"]
}

df=pd.DataFrame(data)
st.write(df)


uploaded_files=st.file_uploader("choose from the files",type="csv")

if uploaded_files is not None:
    df=pd.read_csv(uploaded_files)
    st.write(df)