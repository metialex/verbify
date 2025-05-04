import streamlit as st

from core.utils import check_login, signup


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title('Welcome to :violet[Verbify]')
    choice = st.selectbox('Login/Signup', ('Login', 'Sign Up'))
    if choice == 'Login':
        username = st.text_input(
            label='Username',
            label_visibility='collapsed',
            value='',
            placeholder='Enter your username')
        password = st.text_input(
            label='Password',
            label_visibility='collapsed',
            value='',
            placeholder='Enter password',
            type='password')
        st.button('Login', type='primary', on_click=logged_in_clicked, args=(username, password))
    else:
        username = st.text_input(
            label='Username',
            label_visibility='collapsed',
            value='',
            placeholder='Enter unique username')
        password = st.text_input(
            label='Password',
            label_visibility='collapsed',
            value='',
            placeholder='Create password',
            type='password')
        st.button('Create my account', type='primary', on_click=sign_up_clicked, args=(username, password))

def logout():
    st.session_state.logged_in = False
    st.rerun()

def sign_up_clicked(username, password):
    if signup(username, password):
        st.session_state['logged_in'] = True
    else:
        st.error("This username already used")

def logged_in_clicked(username, password):
    if check_login(username, password):
        st.toast(f'Hello, {username}!', icon='😍')
        st.session_state['logged_in'] = True
    else:
        st.error("Invalid username or password")

login_page = st.Page(page=login)
logout_page = st.Page(page=logout, title="Log out", icon=":material/logout:")
settings_page = st.Page(page="pages/settings.py", title="Settings", icon=":material/settings:")
training_page = st.Page(
    page="pages/training.py",
    title="Training",
    default=True
)
dictionary_page = st.Page(page="pages/dictionary.py", title="Dictionary")
statistic_page = st.Page(page="pages/statistic.py", title="Statistic")

account_pages = [logout_page, settings_page]
verbify_pages = [training_page, dictionary_page, statistic_page]

if st.session_state.logged_in:
    pg = st.navigation(pages={"Account": account_pages, "Verbify": verbify_pages})
else:
    pg = st.navigation(pages=[login_page])

pg.run()
