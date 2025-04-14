import streamlit as st
import time
from gpt import gpt_generate_hint,gpt_set_client
import pandas as pd
import os

st.set_page_config(page_title="Login", page_icon="🔑")

def login_section():
    # Dummy credentials (Replace with a real authentication system)
    USER_CREDENTIALS = {"admin": "password123", "user": "1234"}

    if not st.session_state["logged_in"]:

        # Input fields for username and password
        username = st.text_input("Username",placeholder="Type your username",key=100)
        password = st.text_input("Password", type="password",placeholder="Type your username",key=200)

        if st.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                #Initialize all necessary state variables
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state.gpt_client = gpt_set_client()
                st.session_state.exit_flag = True
                st.session_state.disabled = False

                #Dictionary related variables
                st.session_state.dictionary = pd.read_json("dict/dictionary.json")
                st.session_state.dict_show_button = False
                st.session_state.prev_german_wrd = ""
                st.session_state.def_form_values = [""] * 4 #Default values for the form. 
                
                #Statistic related variables
                stat_file_location = "statistic_data/user.pkl"
                #Create if not exists
                if not os.path.exists(stat_file_location):
                    statistic_dict = {"idx":[],"date":[],"word":[],"success":[],"learned":[]}
                    pd.DataFrame(data=statistic_dict).to_pickle(stat_file_location)                    
                st.session_state.statistic = pd.read_pickle(stat_file_location)
                if len(st.session_state.statistic) < 1: st.session_state.next_practice_idx = 0
                else: st.session_state.next_practice_idx = st.session_state.statistic["idx"].iloc[-1]+1

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