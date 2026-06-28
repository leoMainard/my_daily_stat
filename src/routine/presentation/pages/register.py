import streamlit as st

from routine.presentation.callbacks.register_callbacks import register

st.title("Créer votre compte")

left, right = st.columns(2)
first_name = left.text_input("Prénom")
last_name = right.text_input("Nom")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")
password_confirm = st.text_input("Confirmer le mot de passe", type="password")

if st.button("Créer le compte", type="primary", shortcut="Enter"):
    register(first_name, last_name, email, password, password_confirm)
