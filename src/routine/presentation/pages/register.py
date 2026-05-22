import time

import streamlit as st
from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository
from routine.domain.exceptions import UserAlreadyExistsError
from routine.domain.services.user_service import UserService

st.title("Créer votre compte")

left, right = st.columns(2)
first_name = left.text_input("Prénom")
last_name = right.text_input("Nom")


email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")
password_confirm = st.text_input("Confirmer le mot de passe", type="password")

if st.button("Créer le compte", type="primary", shortcut="Enter"):
    service = UserService(UserRepository(get_cached_connection()))
    try:
        user = service.register_user(first_name, last_name, email, password, password_confirm)
        st.toast("Account created successfully!", icon=":material/check:")
        with st.spinner("Redirection vers la page de connexion ..."):
            time.sleep(2)
            st.switch_page("pages/login.py")
    except ValueError as exc:
        st.toast(str(exc), icon=":material/warning:")
    except UserAlreadyExistsError:
        st.toast("Un compte existe déjà avec cet email", icon=":material/warning:")