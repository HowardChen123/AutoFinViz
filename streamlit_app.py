import streamlit as st
import openai
import pandas as pd

st.title('AutoFinViz')

# OpenAI API Key Input
openai_api_key = st.text_input('Enter your OpenAI API key', type='password')

# Save the API key in the config file if it's entered
if openai_api_key:
    openai.api_key = openai_api_key
    st.success('API Key saved!')

# File Uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# If a file is uploaded, read it into a DataFrame
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Display the DataFrame
    st.write(df)

# File Uploader
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# # If a file is uploaded, read it into a DataFrame
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     # Display the DataFrame
#     st.write(df)