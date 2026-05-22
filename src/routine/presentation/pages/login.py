import time

import streamlit as st

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository



st.title("Connexion")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")

if st.button("Connexion", type="primary", shortcut="Enter"):
    if email and password:
        if '@' not in email:
            st.toast("Email invalide", icon=":material/warning:")
            st.stop()
        
        db_adapter = get_cached_connection()
        repo = UserRepository(db_adapter)
        user = repo.find_by_email(email)

        if user and user.check_password(password):
            st.session_state.user = user.to_dict()  # Stockage de l'utilisateur dans la session
            st.toast("Connexion réussie! Bienvenue " + user.firstname + "!", icon=":material/check:")
            with st.spinner("Redirection vers le menu..."):
                time.sleep(2)
                st.switch_page("pages/menu.py")
        else:
            st.toast("Email ou mot de passe invalide", icon=":material/warning:")


