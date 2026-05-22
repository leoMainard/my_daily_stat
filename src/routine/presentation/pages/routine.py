import streamlit as st
from routine.config.logger import logger
from routine.utils.streamlit_dialogs import add_stat, display_stat
       

st.write("# Mes routines")

# récupère toutes les routines
routines = st.session_state.get("routines", [])

# on ajoute en premier un "pseudo-routine" qui servira au bouton +
all_buttons = [{"name": "+", "type": "add"}] + routines

st.date_input(label = "Date",value = "today", key = "selected_date", format='DD/MM/YYYY', max_value='today', )

# layout : 5 colonnes fixes
columns = st.columns(5)

for index, routine in enumerate(all_buttons):
    with columns[index % 5]:
        if routine["type"] == "add":
            if st.button("**+**", key="btn_add_routine", type="primary", width="stretch"):
                add_routine()
        else:
            if st.button(f"{routine['name']}", key=f"routine_button_{index}", width="stretch"):
                display_routine(routines_infos = routine)