import streamlit as st
from my_daily_stat.config.logger import logger
from my_daily_stat.utils.streamlit_dialogs import add_stat, display_stat
       

st.write("# Welcome to My Daily Stat! 👋")

# récupère toutes les stats
stats = st.session_state.get("stat", [])

# on ajoute en premier un "pseudo-stat" qui servira au bouton +
all_buttons = [{"name": "+", "type": "add"}] + stats

st.date_input(label = "Date",value = "today", key = "selected_date", format='DD/MM/YYYY', max_value='today', )

# layout : 5 colonnes fixes
columns = st.columns(5)

for index, stat in enumerate(all_buttons):
    with columns[index % 5]:
        if stat["type"] == "add":
            if st.button("**\+**", key="btn_add_stat", type="primary", width="stretch"):
                add_stat()
        else:
            if st.button(f"{stat['name']}", key=f"stat_button_{index}", width="stretch"):
                display_stat(stats_infos = stat)