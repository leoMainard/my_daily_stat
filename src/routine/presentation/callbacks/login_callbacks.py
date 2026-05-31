import streamlit as st
import time

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository
from routine.domain.exceptions import AuthenticationError
from routine.domain.services.user_service import UserService

def login(email: str, password: str):
    service = UserService(UserRepository(get_cached_connection()))
    try:
        user = service.authenticate(email, password)
        st.session_state.user = user.to_dict()
        with st.spinner("Redirection vers le menu principal ..."):
            time.sleep(1)
            st.switch_page("pages/menu.py")
    except AuthenticationError:
        st.toast("Invalid email or password", icon=":material/warning:")