import streamlit as st 
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import SmartDataframe
from time import sleep
import numpy as np


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(layout='wide')

box = st.empty()
data = pd.read_csv("./Success v0.5.csv")

def chat_with_csv(df,prompt):
    llm = OpenAI(api_token=openai_api_key)
    df = SmartDataframe(df, config={"llm": llm})
    result = df.chat(prompt)
    return result

def login():
    with box.container():
        st.title("Login")
        st.session_state.option = st.selectbox("Which shipping line are you from?", data["Shipping Line"].unique())
        st.button("Submit", type="primary", on_click=handle_login)

def handle_login():
    st.session_state.login = True
    box.empty() 
    sleep(0.01)

def chat_page():
    with box.container():
        st.title("Request Containers")
        st.write("Logged in as ", st.session_state.option)

        col1, col2 = st.columns([1,1])

        with col1:
            data = pd.read_csv("./Success v0.5.csv")
            data = data[(data['Available'] == 1)]
            del data['Available']
            st.dataframe(data.set_index(data.columns[0]), use_container_width=True)

        with col2:
            containers_need = st.number_input("How many containers do you need?", min_value=1, max_value=999999, value=1)
            line_options = np.insert(data["Shipping Line"].unique(), 0, "Any")
            line = st.selectbox("Shipping line to borrow from", line_options[line_options != st.session_state.option])
            container_options = np.insert(data["Type"].unique(), 0, "Any")
            container_type = st.selectbox("Select container type", container_options)
                
            if containers_need is not None:
                st.session_state.containers = containers_need
                prompt = "Give me the list of the " + str(containers_need) + " least expensive "
                if container_type is not "Any":
                    prompt += container_type
                prompt += " containers"
                if line is not "Any":
                    prompt += " from " + line
                prompt += "."
                if st.button("Submit"):
                    st.info("Your Query: "+prompt)
                    st.session_state.result = chat_with_csv(data, prompt)

def confirm_page(result):
    with box2.container():
        st.title("Check results")
        if st.button("Clear"):
            st.session_state.result = None
            box2.empty()
            sleep(0.01)
        if result is not None:
            st.dataframe(result.set_index(result.columns[0]), use_container_width=True)
        if len(result.index) < st.session_state.containers:
            st.error("Found only " + str(len(result.index)) + " containers. Consider relaxing your search requirements.")
        st.success("Total price: $" + str(result['Price'].sum()))
        confirm = st.button("Place Order")
        if confirm:
            st.balloons()
            st.toast("Order placed successfully")

if 'login' not in st.session_state:
    st.session_state.login = False
if 'result' not in st.session_state:
    st.session_state.result = None

login()

if st.session_state.login:
    chat_page()

if st.session_state.result is not None:
    box2 = st.empty()
    confirm_page(st.session_state.result.dataframe)

