import streamlit as st
import time
from gpt import gpt_generate_hint,gpt_set_client
import pandas as pd

def login_section():
    # Dummy credentials (Replace with a real authentication system)
    USER_CREDENTIALS = {"admin": "password123", "user": "1234"}

    if not st.session_state["logged_in"]:

        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                #Initialize all necessary state variables
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state.dictionary = pd.read_json("dict/dictionary.json")
                st.session_state.gpt_client = gpt_set_client()
                st.session_state.exit_flag = True
                st.session_state.disabled = False
                st.session_state.dict_show_button = False
                st.session_state.prev_german_wrd = ""
                st.session_state.eng_def = st.session_state.rus_def = st.session_state.type_def = st.session_state.art_def = ""
                st.success(f"Welcome, {username}, your dictionary and GPT assistant configured!")
                time.sleep(1)
                st.rerun()  # Refresh the page
            else:
                st.error("Invalid username or password!")
    else:
        st.write(f"Hello, **{st.session_state['username']}**! You are logged in.")
        
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

st.title("Login Page")
login_section()