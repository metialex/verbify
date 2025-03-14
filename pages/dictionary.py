import streamlit as st
import time
from util import util_capit,util_add_word
import pandas as pd
from gpt import gpt_generate_word_by_german

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
   
    st.title("Add a new word to the dictionary")
    col1,col2 = st.columns(2)

    with col1:
        german_word = util_capit(st.text_input("German word:", "",placeholder = "Fill and press enter for GPT autofill"))
        if german_word != "" and st.session_state.prev_german_wrd != german_word:
            gpt_output = gpt_generate_word_by_german(german_word)
            try:
                if gpt_output.split(",")[0] != "x": st.session_state.eng_def = gpt_output.split(",")[0]
                if gpt_output.split(",")[1] != "x": st.session_state.rus_def = gpt_output.split(",")[1]
                if gpt_output.split(",")[2] != "x": st.session_state.type_def = gpt_output.split(",")[2]
                if gpt_output.split(",")[3] != "x": st.session_state.art_def = gpt_output.split(",")[3]
            except:
                st.write("GPT output is with wrong format")
        st.session_state.prev_german_wrd = german_word

        english_word = st.text_input("English word:",st.session_state.eng_def)
        russian_word = st.text_input("Russian word:", st.session_state.rus_def)
        word_type = st.text_input("Word type:", st.session_state.type_def)
        article = st.text_input("Article:", st.session_state.art_def)
        tags = st.text_input("Tags: tag_1,tag_2,...").split(",")
        if st.button("Add word"):
            st.session_state.dictionary =util_add_word(german_word,
                                                    english_word,
                                                    article,
                                                    russian_word,
                                                    word_type,
                                                    tags,
                                                    st.session_state.dictionary)
            
            st.session_state.dictionary.to_json('dict/dictionary.json', force_ascii=False)
            st.success(f"Word have been added!")
            time.sleep(2)
            st.rerun()


    #Search over dictionary by english word
    df = st.session_state.dictionary

    st.write("Search and edit by english word")

    # User input to search by name
    name = st.text_input("Enter Name to Search", "")

    if name:
        # Find row matching the name
        row = df[df["english"].str.contains(name, na=False, case=False)]

        if not row.empty:
            st.write("Record Found. Edit Below:")

            # Convert the row to a dictionary
            row_idx = row.index[0]  # Get the index of the row
            edited_data = st.data_editor(row, key="editor")

            # Update the main DataFrame with the edited values
            if st.button("Save Changes"):
                df.loc[row_idx] = edited_data.iloc[0]  # Update only that row
                st.session_state["df"] = df  # Store the updated DataFrame
                st.session_state.dictionary.to_json('dict/dictionary.json', force_ascii=False)
                st.success("Changes saved successfully!")

        else:
            st.warning("No record found with that name.")

    if st.button("Show/hide dictionary"):
        st.session_state.dict_show_button = not st.session_state.dict_show_button
    
    if st.session_state.dict_show_button:
        # Editable DataFrame
        edited_df = st.data_editor(df, num_rows="dynamic")  # Users can edit and add rows
    
        if st.button("Save dictionary"):
            st.session_state.dictionary = edited_df
            edited_df.to_json('dict/dictionary.json', force_ascii=False)
            
    
else: st.write("Please, login")