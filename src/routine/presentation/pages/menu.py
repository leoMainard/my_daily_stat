import streamlit as st

st.title("👋 Bienvenue " + st.session_state.user["firstname"] + " !" if "user" in st.session_state else "")