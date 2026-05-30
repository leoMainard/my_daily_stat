import time

import streamlit as st

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository
from routine.domain.exceptions import AuthenticationError
from routine.domain.services.user_service import UserService



st.title("Connexion")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")

if st.button("Connexion", type="primary", shortcut="Enter"):
    service = UserService(UserRepository(get_cached_connection()))
    try:
        user = service.authenticate(email, password)
        st.session_state.user = user.to_dict()
        with st.spinner("Redirection vers le menu principal ..."):
            time.sleep(1)
            st.switch_page("pages/menu.py")
    except AuthenticationError:
        st.toast("Invalid email or password", icon=":material/warning:")


