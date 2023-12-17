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

    # Display the dataset description
    st.markdown("### Dataset Description")
    st.write(summary['dataset_description'])

    # Display each field with its properties
    st.markdown("### Field Details")
    for field in summary['fields']:
        column_name = field['column']
        properties = field['properties']

        st.markdown(f"#### {column_name}")
        st.json(properties)

    time.sleep(60)
    
    # Run question formulation
    question_formulations = pipeline.formulate_questions(summary, category, 3)

    # Displaying the data using Markdown
    st.markdown("### Question Formulations")

    for question in question_formulations:

        x_axis = question['x_axis'] if isinstance(question['x_axis'], list) else [question['x_axis']]
        y_axis = question['y_axis'] if isinstance(question['y_axis'], list) else [question['y_axis']]

        st.markdown(f"""
        #### Question {question['index']}: {question['title']}
        - **Visualization Type:** {question['visualization_type']}
        - **X-axis:** {', '.join(x_axis)}
        - **Y-axis:** {', '.join(y_axis)}
        """)
        st.markdown("---")  # Adding a separator line