import streamlit as st
import openai
import pandas as pd
from autofinviz.components.pipeline import Pipeline
import os
from autofinviz.utils import json_to_readable
import time

st.title('AutoFinViz')

# Using session state to track whether the key has been submitted
if 'key_submitted' not in st.session_state:
    st.session_state.key_submitted = False

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

if 'df' not in st.session_state:
    st.session_state.df = None

# OpenAI API Key Input
if not st.session_state.key_submitted:
    with st.form("api_key_form"):
        openai_api_key = st.text_input('Enter your OpenAI API key', type='password')
        submit_key = st.form_submit_button('Submit API Key')

    if submit_key and openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        st.session_state.key_submitted = True
        st.success('API Key saved!')

# File Uploader
if st.session_state.key_submitted and not st.session_state.file_uploaded:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.file_uploaded = True
        st.write(st.session_state.df)  # Display the DataFrame

if st.session_state.key_submitted and st.session_state.file_uploaded and st.session_state.df is not None:
    # Extract df_name from the file path
    df_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]

    pipeline = Pipeline()

    # Run summarize method and get the summary
    category = pipeline.classify(st.session_state.df)

    time.sleep(60)

    # Run summarize method and get the summary
    summary, st.session_state.df = pipeline.summarize(st.session_state.df, df_name=df_name, category=category)

    # Display the returned summary in a form
    st.write("Summary:")
    st.write(json_to_readable(summary))
