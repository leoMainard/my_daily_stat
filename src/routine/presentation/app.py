import streamlit as st


st.set_page_config(layout="centered")

if "user" not in st.session_state:
    pages = [
        st.Page("pages/menu.py", title="Menu", icon=":material/home:"),
        st.Page("pages/login.py", title="Connexion", icon=":material/login:"),
        st.Page("pages/register.py", title="Inscription", icon=":material/person_add:"),
    ]
else:
    pages = [
        st.Page("pages/menu.py", title="Menu", icon=":material/home:"),
        st.Page("pages/routine.py", title="Mes routines", icon=":material/add_circle:"),
        st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
        st.Page("pages/sign_out.py", title="Déconnexion", icon=":material/logout:")
    ]

pg = st.navigation(pages, position="top")
pg.run()