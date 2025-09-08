import streamlit as st


# st.set_page_config(layout="wide")

pages = [
    st.Page("pages/add_stats.py", title="Add stats"),
    st.Page("pages/dashboard.py", title="Dashboard")
]

pg = st.navigation(pages, position="top")
pg.run()