import streamlit as st

def apply_style():
    st.markdown("""
        <style>
            /* User message */
            div[data-testid="stChatMessage"] {
                background-color: #333333 !important;
                color: white !important;
                border-radius: 10px;
                padding: 10px;
            }

            /* Assistant message */
            div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="assistant"]) {
                background-color: #333333 !important;  /* Dark gray for assistant */
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .custom-text {
                position: absolute;
                top: 50px;
                left: 200px;
                font-size: 14px;
                background-color: #333333;
                padding: 5px;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            /* Apply background color to main content area */
            .stApp {
                background-color: #333333 !important;
            }
             /* Ensure all markdown and text elements use white text */
            .stMarkdown, .stTextInput, .stButton, .stSelectbox, .stCheckbox {
                color: white !important;
            }

            /* Adjust buttons and inputs to fit the theme */
            .stTextInput>div>div>input, .stSelectbox>div>div>select {
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                caret-color: white !important;
            }

            .stButton>button {
                background-color: white !important;
                color: #333333 !important;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            .st-emotion-cache-1ghhuty ea2tk8x3{
                color: black !important;
            }
            h1 {
                    color: white !important;
                    font-size: 30px !important;
            }
            section[data-testid="stSidebar"] {
                background-color: #333333;  /* Dark Blue */
            }

        </style>
        """, unsafe_allow_html=True)
