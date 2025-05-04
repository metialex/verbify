import streamlit as st
import pandas as pd
import time

from core import gpt, utils

st.title("Training")

# Initialize all necessary state variables
st.session_state.dictionary = pd.read_json("data/dictionary.json")
st.session_state.gpt_client = gpt.gpt_set_client() # !!! REWORK !!!
st.session_state.exit_flag = True
st.session_state.disabled = False
st.session_state.dict_show_button = False
st.session_state.prev_german_wrd = ""
st.session_state.eng_def = st.session_state.rus_def = st.session_state.type_def = st.session_state.art_def = ""

# Create columns
col1, col2, col3, col4 = st.columns(4)

# Place segmented controls in each column
with col1:
    st.session_state.practice_lang = "german"
    st.session_state.origin_lang = st.segmented_control(
        "Language",
        ["english", "german"],
        default="english",
        disabled=st.session_state.disabled
    )
    if st.session_state.origin_lang == "english": st.session_state.practice_lang = "german"
    elif st.session_state.origin_lang == "german": st.session_state.practice_lang = "english"
with col2:
    st.session_state.w_n = st.segmented_control(
        "Number of words",
        [3, 20, 30],
        default=20,
        disabled=st.session_state.disabled
    )
with col3:
    st.session_state.acc = st.segmented_control(
        "Accuracy (%)",
        [100, 50, 20],
        default=50,
        disabled=st.session_state.disabled
    )
with col4:
    st.session_state.learned = st.segmented_control(
        "Learned",
        [False,True],
        default=False,
        disabled=st.session_state.disabled
    )

if st.button("Start practice", type='primary', disabled=st.session_state.disabled):
    st.session_state.exit_flag = False
    st.session_state.disabled = True
    st.session_state.idx_list = []
    st.session_state.word_counter = 0

    #Read the dictionary and prepare the list of words
    for index, word in st.session_state.dictionary.sample(frac=1).iterrows():
        if len(st.session_state.idx_list) >= st.session_state.w_n: break
        word_accuracy = (word['num_success'] / word['num_practiced'] * 100) if word['num_practiced'] else 0.01
        if word_accuracy >= st.session_state.acc:
            if ((not st.session_state.learned and word["learned"] != True )
            or st.session_state.learned):
                st.session_state.idx_list.append(index)
    st.rerun()

if (st.session_state.disabled
    and st.session_state.word_counter < len(st.session_state.idx_list)
    and st.session_state.exit_flag != True):

    st.write(st.session_state.word_counter)

    practice_lang = st.session_state.practice_lang
    origin_lang = st.session_state.origin_lang

    wrd_idx = st.session_state.idx_list[st.session_state.word_counter]
    # Wrd gives a copy, while dictionary allows to access directly to the instance
    wrd = st.session_state.dictionary.iloc[wrd_idx]
    dictionary = st.session_state.dictionary

    prompt = f"<span style='font-size: 20px;'>{wrd[origin_lang]}</span>"
    st.write('translate to ' + practice_lang + " - " + prompt, unsafe_allow_html=True)

    # Define the correct answer
    correct_string = wrd[practice_lang]
    if wrd['type'] == "Verb" and len(correct_string.split()) > 1:
        correct_string = utils.capitalize(correct_string.split()[1])

    was_correct = None
    with st.chat_message('user'):
        my_word = st.chat_input("Enter your word")

    if my_word is None:
        st.write("The hint will be visible here")
    else:
        # Cases without additional action
        if my_word == "0":
            st.session_state.exit_flag = True
            st.write("<span style='color:red;'>Stop the practice</span>", unsafe_allow_html=True)
            time.sleep(3)
            st.rerun()
        elif my_word == "1":
            label = correct_string[0] + "*" * (len(correct_string) - 2) + correct_string[-1]
            st.write(label, unsafe_allow_html=True)
        elif my_word == "2":
            gpt.gpt_generate_hint(wrd, origin_lang)
        # Cases with writing word statistic
        elif my_word == "+":
            dictionary.loc[wrd_idx, 'learned'] = True
            dictionary.loc[wrd_idx, 'num_practiced'] += 1
            st.session_state.word_counter += 1
            st.write(f"<span style='color:green;'>Word {correct_string} is marked as known</span>",
                     unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        elif my_word == correct_string or utils.capitalize(my_word) == correct_string:
            dictionary.loc[wrd_idx, 'num_practiced'] += 1
            dictionary.loc[wrd_idx, 'num_success'] += 1
            dictionary.loc[wrd_idx, 'last_success'] = 1
            st.session_state.word_counter += 1
            st.write(f"<span style='color:green;'>Correct</span>", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        else:
            dictionary.loc[wrd_idx, 'num_practiced'] += 1
            dictionary.loc[wrd_idx, 'last_success'] = 0
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

# Restart the test
if "word_counter" in st.session_state:
    if st.session_state.word_counter == len(st.session_state.idx_list):
        st.success("Test Finished!")
        if st.button("New run"):
            st.session_state.exit_flag = False
            st.session_state.disabled = False
            st.session_state.dictionary.to_json('data/dictionary.json', force_ascii=False)
            st.rerun()
