from openai import OpenAI
from termcolor import colored
import streamlit as st

#ChatGPT setup
def gpt_set_client(key_loc = "/Users/metialex/my_applications/api_keys/openai.txt" ):

    with open(key_loc, "r") as file:
        key_str = file.readline().strip()
    try:
        client = OpenAI(api_key=key_str)
    except:
        print(colored('No internet connection'),'red')
        client = False
    return client

def gpt_generate_hint(wrd, orig_lang):
    try:
        completion = st.session_state.gpt_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    store=True,
                    messages=[
                        {"role": "user", "content": f"Provide a short sentence in {orig_lang} which contain the word {wrd[orig_lang]}. Make this sentence within B1 level"}
                    ]
                    )
        label = f"Example of usage - {completion.choices[0].message.content}"
        st.write(label, unsafe_allow_html=True)
    except:
        st.write('Connection problem, example cannot be generated')