import streamlit as st

st.title("👋 Salut " + st.session_state.user["firstname"] + " !" if "user" in st.session_state else "👋 Bienvenue")

st.session_state