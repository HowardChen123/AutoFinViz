import streamlit as st
import openai
import pandas as pd
from autofinviz.components.pipeline import Pipeline
import os

st.title('AutoFinViz')

# Using session state to track whether the key has been submitted
if 'key_submitted' not in st.session_state:
    st.session_state.key_submitted = False

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

# OpenAI API Key Input
if not st.session_state.key_submitted:
    with st.form("api_key_form"):
        openai_api_key = st.text_input('Enter your OpenAI API key', type='password')
        submit_key = st.form_submit_button('Submit API Key')

    if submit_key and openai_api_key:
        openai.api_key = openai_api_key
        st.session_state.key_submitted = True
        st.success('API Key saved!')

# File Uploader
if st.session_state.key_submitted and not st.session_state.file_uploaded:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.file_uploaded = True
        # Display the DataFrame
        st.write(df)
        # Extract df_name from the file path
        df_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]

if st.session_state.key_submitted and st.session_state.file_uploaded:
    pipeline = Pipeline()

    # Run summarize method and get the summary
    summary, df = pipeline.summarize(df, df_name=df_name, category="Market Data")

    # Display the returned summary in a form
    with st.form("summary_form"):
        st.write("Summary:")
        st.write(summary)
        st.form_submit_button('Confirm Summary')
