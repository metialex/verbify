from openai import OpenAI
import streamlit as st

#ChatGPT setup
def gpt_set_client(key_loc = "/Users/metialex/my_applications/api_keys/openai.txt" ):

    with open(key_loc, "r") as file:
        key_str = file.readline().strip()
    try:
        client = OpenAI(api_key=key_str)
    except:
        st.write("Error with set up GPT client")
        client = False
    return client

def gpt_generate_hint(wrd, orig_lang):
    try:
        completion = st.session_state.gpt_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    store=True,
                    messages=[
                        {"role": "user", "content": f"Provide a short sentence in {orig_lang} which" \
                         "contain the word {wrd[orig_lang]}. Make this sentence within B1 level"}
                    ]
                    )
        label = f"Example of usage - {completion.choices[0].message.content}"
        st.write(label, unsafe_allow_html=True)
    except:
        st.write('Connection problem, example cannot be generated')

def gpt_generate_word_by_german(wrd):
    try:
        completion = st.session_state.gpt_client.chat.completions.create(
                    model="gpt-4o",
                    store=True,
                    messages=[
                        {"role": "user", "content": f"For the gemrman word '{wrd}' give the following output:"\
                            "e_t,r_t,w_t_e,g_a. e_t is english translation of the word, r_t is russian translation of the word,"\
                            "w_t_e is the word type in english and g_a is german article (if the word is not noun, make the article 'x')"
                            "Within e_t,r_t and g_a first letters should be capitilized."\
                            "Avoid 'e_t:value' format, give only direct values for output."
                            "In case if there is no such a german word, return 'x,x,x,x'"}
                    ]
                    )
        return completion.choices[0].message.content
    except:
        st.write('Connection problem, autofill cannot be completed')