import time

import bcrypt
import streamlit as st
from routine.config.enums import UserRole
from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.user_repository import UserRepository
from routine.domain.models.user import User

st.title("Créer votre compte")

left, right = st.columns(2)
first_name = left.text_input("Prénom")
last_name = right.text_input("Nom")


email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")
password_confirm = st.text_input("Confirmer le mot de passe", type="password")

if st.button("Créer le compte", type="primary", shortcut="Enter"):
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
                st.toast("Un compte avec cet email existe déjà", icon=":material/warning:")
                st.stop()
            user = repo.create(user)

            if user.id:
                st.toast("Compte créé avec succès! Bienvenue " + user.firstname + "!", icon=":material/check:")
                with st.spinner("Redirection vers la page de connexion..."):
                    time.sleep(2)
                    st.switch_page("pages/login.py")
            else:
                st.toast("Échec de la création du compte", icon=":material/cancer:")
        else:
            st.toast("Les mots de passe ne correspondent pas", icon=":material/warning:")
    else:
        st.toast("Veuillez remplir tous les champs", icon=":material/warning:")