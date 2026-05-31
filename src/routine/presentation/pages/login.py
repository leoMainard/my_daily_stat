import streamlit as st

from routine.presentation.callbacks.login_callbacks import login

st.title("Connexion")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")

if st.button("Connexion", type="primary", shortcut="Enter"):
    login(email, password)


