import time

import streamlit as st

from my_daily_stat.db.adapters.postgres import get_cached_connection
from my_daily_stat.db.repositories.user_repository import UserRepository



st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login", type="primary", shortcut="Enter"):
    if email and password:
        if '@' not in email:
            st.toast("Email invalide", icon=":material/warning:")
            st.stop()
        
        db_adapter = get_cached_connection()
        repo = UserRepository(db_adapter)
        user = repo.find_by_email(email)

        if user and user.check_password(password):
            st.session_state.user = user.to_dict()  # Stockage de l'utilisateur dans la session
            st.toast("Login successful! Welcome " + user.firstname + "!", icon=":material/check:")
            with st.spinner("Redirecting to menu..."):
                time.sleep(2)
                st.switch_page("pages/menu.py")
        else:
            st.toast("Invalid email or password", icon=":material/warning:")


