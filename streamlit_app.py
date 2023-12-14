import streamlit as st
import openai
import pandas as pd

st.title('AutoFinViz')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

submit_key = st.button('Submit')

if submit_key:

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if openai_api_key:
        openai.api_key = openai_api_key
        st.success('API Key saved!')

# File Uploader
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# # If a file is uploaded, read it into a DataFrame
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     # Display the DataFrame
#     st.write(df)