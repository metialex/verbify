import streamlit as st
import os
from termcolor import colored
import time
import argparse
from tqdm import tqdm
import util
from gpt import gpt_generate_hint,gpt_set_client
from openai import OpenAI
import pandas as pd

from pages.login import login_section

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    # Session state to track progress

    # Create four columns
    col1, col2, col3 = st.columns(3)

    # Place segmented controls in each column
    with col1: 
        st.session_state.pract_lang = "german"
        st.session_state.orig_lang = st.segmented_control("Language", ["english", "german"],default="english",disabled=st.session_state.disabled)
        if st.session_state.orig_lang == "english": st.session_state.pract_lang = "german"
        elif st.session_state.orig_lang == "german": st.session_state.pract_lang = "english" 
    with col2: st.session_state.w_n = st.segmented_control("Number of words", [3, 20, 30],default=20,disabled=st.session_state.disabled)
    with col3: st.session_state.acc = st.segmented_control("Accuracy (%)", [0, 50, 25],default=0,disabled=st.session_state.disabled)
        
    if st.button("Start practice",disabled=st.session_state.disabled):
        st.session_state.exit_flag = False
        st.session_state.disabled = True
        st.session_state.idx_list = []
        st.session_state.word_counter = 0

        #Read the dictionary and prepare the list of words
        for index, word in st.session_state.dictionary.sample(frac=1).iterrows():
            if len(st.session_state.idx_list) >= st.session_state.w_n: break
            word_accuracy = (word['num_success'] / word['num_practiced'] * 100) if word['num_practiced'] else 0.01
            if word_accuracy >= st.session_state.acc: st.session_state.idx_list.append(index)
        st.rerun()

    if (st.session_state.disabled 
        and st.session_state.word_counter < len(st.session_state.idx_list) 
        and st.session_state.exit_flag != True):

        st.write(st.session_state.word_counter)

        pract_lang = st.session_state.pract_lang
        orig_lang = st.session_state.orig_lang

        wrd_idx = st.session_state.idx_list[st.session_state.word_counter]
        
        wrd = st.session_state.dictionary.iloc[wrd_idx]
        
        prompt = f"<span style='font-size: 20px;'>{wrd[orig_lang]}</span>"
        st.write( 'translate to ' + pract_lang + " - " + prompt, unsafe_allow_html=True)
        
        #Define the correct answer
        correct_string = wrd[pract_lang]
        if wrd['type'] == "Verb" and len(correct_string.split()) > 1:
            correct_string = util.util_capit(correct_string.split()[1])

        was_correct = None
        with st.chat_message('user'):
            my_word = st.chat_input("Enter your word")

        if my_word is None:
            st.write("The hint will be visible here")
        else:
            #Cases without additional action
            if my_word == "0":
                st.session_state.exit_flag = True
                st.write("<span style='color:red;'>Stop the practice</span>", unsafe_allow_html=True)
                time.sleep(3)
                st.rerun()
            elif my_word == "1":
                label = correct_string[0] + "*" * (len(correct_string)-2) + correct_string[-1]
                st.write(label, unsafe_allow_html=True)
            elif my_word == "2":
                gpt_generate_hint(wrd,orig_lang)
            #Cases with writing word statistic
            elif my_word == "+":
                wrd['learned'] = True
                wrd['num_practiced'] += 1
                st.session_state.word_counter += 1
                st.write(f"<span style='color:green;'>Word {correct_string} is marked as known</span>", unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            elif my_word == correct_string or util.util_capit(my_word) == correct_string:
                wrd['num_practiced'] += 1
                wrd['num_success'] += 1
                wrd['last_success'] = 1
                st.session_state.word_counter += 1
                st.write(f"<span style='color:green;'>Correct</span>", unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            else:
                wrd['num_practiced'] += 1
                wrd['last_success'] = 0
                st.session_state.word_counter += 1
                st.session_state.idx_list.append(wrd_idx)
                st.write(f"<span style='color:red;'>'Failed' + ' - ' + {correct_string}</span>", unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
        
        st.markdown("""
            <div class="custom-text"><span style="white-space:pre-line;">1 - gives an amount of letters in word  
            2 - gives a GPT generated example  
            '+' - marks word as learned  
            </span>
        """, unsafe_allow_html=True)
    
    #Restart the test
    if "word_counter" in st.session_state:
        if st.session_state.word_counter == len(st.session_state.idx_list):
            st.success("Test Finished!")
            if st.button("New run"):
                st.session_state.exit_flag = False
                st.session_state.disabled = False
                st.rerun()

else:
    col1, col2, col3 = st.columns(3)
    with col2: login_section()
