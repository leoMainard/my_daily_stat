import streamlit as st

from streamlit_cookies_controller import CookieController

CookieController().remove("session")
del st.session_state["user"]
st.switch_page("pages/menu.py")
