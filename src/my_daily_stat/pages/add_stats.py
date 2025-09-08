import streamlit as st
from my_daily_stat.utils.streamlit_dialogs import add_stat

st.write("# Welcome to My Daily Stat! 👋")

# récupère toutes les stats
stats = st.session_state.get("stat", [])

# on ajoute en premier un "pseudo-stat" qui servira au bouton +
all_buttons = [{"name": "+", "type": "add"}] + stats

# layout : 5 colonnes fixes
columns = st.columns(5)

for index, stat in enumerate(all_buttons):
    with columns[index % 5]:
        if stat["type"] == "add":
            if st.button("**\+**", key="btn_add_stat", type="primary"):
                add_stat()
        else:
            if st.button(f"{stat['name']} ({stat['type']})", key=f"stat_button_{index}"):
                st.write(f"You clicked on {stat['name']} of type {stat['type']}")