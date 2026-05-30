import streamlit as st

from routine.presentation.callbacks.routine_callbacks import load_routines, edition_routine, display_routine

st.write("# Mes routines")

load_routines()

# on ajoute en premier un "pseudo-routine" qui servira au bouton +
all_buttons = [{"name": "+", "type": "add"}] + st.session_state.routines

# layout : 5 colonnes fixes
columns = st.columns(5)

for index, routine in enumerate(all_buttons):
    with columns[index % 5]:
        if routine["type"] == "add":
            if st.button("**+**", key="btn_add_routine", type="primary", width="stretch"):
                edition_routine()
        else:
            if st.button(f"{routine['name']}", key=f"routine_button_{index}", width="stretch"):
                display_routine(routines_infos = routine)

# Edition d'une routine : si une routine a été mise en attente pour édition, on affiche le dialog d'édition avec les infos de la routine à éditer
if st.session_state.get("pending_edit_routine"):
    routine_to_edit = st.session_state.pop("pending_edit_routine")
    edition_routine(routine_infos=routine_to_edit, type="edit")
