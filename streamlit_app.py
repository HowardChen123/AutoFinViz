import streamlit as st
import openai
import pandas as pd

st.title('AutoFinViz')

# Create a form for the OpenAI API Key Input
with st.form("api_key_form"):
    openai_api_key = st.text_input('Enter your OpenAI API key', type='password')
    submit_key = st.form_submit_button('Submit API Key')

if submit_key and openai_api_key:
    openai.api_key = openai_api_key
    st.success('API Key saved!')
else:
    st.stop()

# File Uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Create a DataFrame and display it in a form
    with st.form("dataframe_form"):
        df = pd.read_csv(uploaded_file)
        st.write(df)
        st.form_submit_button('Confirm Data')
else:
    st.stop()