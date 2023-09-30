import streamlit as st 
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import PandasAI

load_dotenv()
#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

openai_api_key = os.getenv("OPENAI_API_KEY")


def chat_with_csv(df,prompt):
    llm = OpenAI(api_token=openai_api_key)
    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df, prompt=prompt)
    print(result)
    return result

def login():
    st.title("Shipping Line Login")
    st.selectbox("Which shipping line are you from?")

def chat_page():
    st.set_page_config(layout='wide')
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

login()
