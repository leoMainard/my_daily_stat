import datetime

import streamlit as st

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.routine_value_repository import RoutineValueRepository
from routine.domain.services.routine_value_service import RoutineValueService
from routine.presentation.callbacks.routine_callbacks import (
    load_routines,
    edition_routine,
    display_routine,
)

service = RoutineValueService(RoutineValueRepository(get_cached_connection()))
load_routines()


st.write("# Mes routines")

# on ajoute en premier un "pseudo-routine" qui servira au bouton +
all_buttons = [{"name": "+", "type": "add"}] + st.session_state.routines


page_routine_date_value: datetime.date = st.date_input(
    label="Date de suivi pour votre routine",
    value="today",
    format="DD/MM/YYYY",
    key="date_routine_generale",
)

# layout : 5 colonnes fixes
columns = st.columns(5)
for index, routine in enumerate(all_buttons):
    with columns[index % 5]:
        if routine["type"] == "add":
            if st.button(
                "**+**", key="btn_add_routine", type="primary", width="stretch"
            ):
                edition_routine()
        else:
            routine_value = service.get_routine_value_by_routine_id_and_date(
                routine["id"], page_routine_date_value
            )
            if st.button(
                f"{routine['name']}",
                key=f"routine_button_{index}",
                width="stretch",
                type="primary"
                if routine_value and routine_value.value is not None
                else "secondary",
            ):
                display_routine(
                    routines_infos=routine, date_value=page_routine_date_value
                )

# Edition d'une routine : si une routine a été mise en attente pour édition, on affiche le dialog d'édition avec les infos de la routine à éditer
if st.session_state.get("pending_edit_routine"):
    routine_to_edit = st.session_state.pop("pending_edit_routine")
    edition_routine(routine_infos=routine_to_edit, type_dialog_routine="edit")
