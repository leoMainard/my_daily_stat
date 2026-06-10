import streamlit as st
import time

from streamlit_cookies_controller import CookieController

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository
from routine.domain.exceptions import AuthenticationError
from routine.domain.services.user_service import UserService
from routine.presentation.utils.session import create_session_token


def login(email: str, password: str):
    service = UserService(UserRepository(get_cached_connection()))
    try:
        user = service.authenticate(email, password)

        user_dict = user.to_dict()
        st.session_state.user = user_dict
        CookieController().set(
            "session", create_session_token(user_dict), max_age=30 * 24 * 60 * 60
        )

        with st.spinner("Redirection vers le menu principal ..."):
            time.sleep(1)
            st.switch_page("pages/menu.py")
    except AuthenticationError:
        st.toast("Invalid email or password", icon=":material/warning:")
