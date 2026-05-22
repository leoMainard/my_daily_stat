import time

import bcrypt
import streamlit as st
from routine.config.enums import UserRole
from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository
from routine.domain.models.user import User

st.title("Create your account")

left, right = st.columns(2)
first_name = left.text_input("Firstname")
last_name = right.text_input("Lastname")

email = st.text_input("Email")
password = st.text_input("Password", type="password")
password_confirm = st.text_input("Confirm Password", type="password")

if st.button("Create Account", type="primary", shortcut="Enter"):
    if first_name and last_name and email and password and password_confirm:
        if password == password_confirm:
            if '@' not in email:
                st.toast("Email invalide", icon=":material/warning:")
        
            if len(first_name) < 2:
                st.toast("Le prénom doit contenir au moins 2 caractères", icon=":material/warning:")
            
            if len(last_name) < 2:
                st.toast("Le nom doit contenir au moins 2 caractères", icon=":material/warning:")
        
            user = User(
                firstname=first_name, 
                lastname=last_name, 
                email=email,
                password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                role=UserRole.USER
            )
            db_adapter = get_cached_connection()
            repo = UserRepository(db_adapter)

            existing_user = repo.find_by_email(email)
            if existing_user:
                st.toast("An account with this email already exists", icon=":material/warning:")
                st.stop()
            user = repo.create(user)

            if user.id:
                st.toast("Account created successfully! Welcome " + user.firstname + "!", icon=":material/check:")
                with st.spinner("Redirecting to login..."):
                    time.sleep(2)
                    st.switch_page("pages/login.py")
            else:
                st.toast("Failed to create account", icon=":material/cancer:")
        else:
            st.toast("Passwords do not match", icon=":material/warning:")
    else:
        st.toast("Please fill in all fields", icon=":material/warning:")