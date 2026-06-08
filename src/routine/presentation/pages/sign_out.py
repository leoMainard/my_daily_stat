import streamlit as st

del st.session_state["user"]
st.switch_page("pages/menu.py")