import streamlit as st


st.set_page_config(layout="wide")

if "user" not in st.session_state:
    pages = [
        st.Page("pages/menu.py", title="Menu", icon=":material/home:"),
        st.Page("pages/login.py", title="Login", icon=":material/login:"),
        st.Page("pages/register.py", title="Register", icon=":material/person_add:"),
    ]
else:
    pages = [
        st.Page("pages/menu.py", title="Menu", icon=":material/home:"),
        st.Page("pages/add_stats.py", title="Add stats", icon=":material/add_circle:"),
        st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
    ]

pg = st.navigation(pages, position="top")
pg.run()