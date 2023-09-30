import streamlit as st 
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import PandasAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(layout='wide')

title = st.title("")
box = st.empty()

def chat_with_csv(df,prompt):
    llm = OpenAI(api_token=openai_api_key)
    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df, prompt=prompt)
    print(result)
    return result

def login():
    title = st.title("Login")
    with box.container():
        st.session_state.option = st.selectbox("Which shipping line are you from?", 
            ("Masersk", "ESP23", "NSA", "USAxChina"))
        st.button("Submit", type="primary", on_click=handle_login)

def handle_login():
    st.session_state.login = True
    box.empty() 
    sleep(0.01)

def chat_page():
    st.title("ChatCSV powered by LLM")

    input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

    if input_csv is not None:

            col1, col2 = st.columns([1,1])

            with col1:
                st.info("CSV Uploaded Successfully")
                data = pd.read_csv(input_csv)
                st.dataframe(data, use_container_width=True)

            with col2:

                st.info("Chat Below")
                
                input_text = st.text_area("Enter your query")

                if input_text is not None:
                    if st.button("Chat with CSV"):
                        st.info("Your Query: "+input_text)
                        result = chat_with_csv(data, input_text)
                        st.success(result)
if 'login' not in st.session_state:
    st.session_state.login = False

login()

if st.session_state.login:
    chat_page()
