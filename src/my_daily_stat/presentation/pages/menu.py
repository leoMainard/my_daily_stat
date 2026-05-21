import streamlit as st

st.title("👋 Welcome " + st.session_state.user["firstname"] + " !" if "user" in st.session_state else "")