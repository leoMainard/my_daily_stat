import streamlit as st

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.routine_repository import RoutineRepository
from routine.domain.exceptions import RoutineAlreadyExistsError, RoutineMissingOptionsError
from routine.domain.services.routine_service import RoutineService

@st.dialog("Nouvelle routine")
def add_routine():
    routine_name = st.text_input(
        label = "Nom de la routine",
        placeholder = "Exemple : Jogging du matin"
    )

    description = st.text_area(
        label = "Description",
        placeholder = "Exemple : Suivre ma routine de jogging du matin pour rester en forme et améliorer ma santé cardiovasculaire."
    )

    type = st.selectbox(
        label = "Type",
        options = ("Text", "Checkbox","Feedback","Multiselect", "Number", "Time")
    )

    multiselect_options = []
    if type == "Multiselect":
        multiselect_options = st.multiselect(
            "Add options", 
            options = ("Example : Football"), 
            accept_new_options=True,
            help="Ajouter les différentes options que vous souhaitez suivre pour cette routine. Par exemple, si votre routine est 'Activités sportives', vous pourriez ajouter des options comme 'Football', 'Basketball', 'Natation', etc. Les guillemets seront automatiquement supprimés pour éviter les problèmes de base de données."
        )

    btn_save_add_routine = st.button(
        label = "Save",
        type = "primary",
        icon = ":material/check:"
    )

    if btn_save_add_routine:
        service = RoutineService(RoutineRepository(get_cached_connection()))
        try:
            routine = service.add_routine(
                user_id=st.session_state.user["id"],
                name=routine_name,
                type=type,
                multiselect_options=multiselect_options,
                tags=[],
                description=description
            )
            st.success(
                body="Votre routine a été ajoutée !", 
                icon="🔥"
            )
        except RoutineMissingOptionsError:
            st.warning(
                body="Les options sont obligatoires pour une routine de type Multiselect", 
                icon="🚨"
            )
        except RoutineAlreadyExistsError:
            st.warning(
                body="Une routine existe déjà avec ce nom pour cet utilisateur", 
                icon="🚨"
            )
        except Exception as e:
            st.error(
                body="Une erreur est survenue ... {}".format(e), 
                icon="🚨"
            )

@st.dialog("Ma routine")
def display_routine(routines_infos: dict):
    # TODO : ajouter la modification d'une routine
    try:
        st.write(f"## {routines_infos['name']}")

        st.badge(routines_infos.get("description", ""), icon=":material/lightbulb_2:" ,color="blue")

        if routines_infos["type"] == "Text":
            user_input = st.text_input(
                label = f"Your {routines_infos['name']}",
                placeholder = f"Example : I did 30 minutes of sport"
            )

        elif routines_infos["type"] == "Checkbox":
            user_input = st.checkbox(
                label = f"Did you {routines_infos['name']} today ?"
            )

        elif routines_infos["type"] == "Feedback":
            user_input = st.feedback(
                options = "faces"
            )

        elif routines_infos["type"] == "Multiselect":
            user_input = st.multiselect(
                label = f"Select your {routines_infos['name']} today",
                options = routines_infos.get("multiselect_option", [])
            )

        elif routines_infos["type"] == "Number input":
            user_input = st.number_input(
                label = f"Your {routines_infos['name']}",
                step=1
            )

        elif routines_infos["type"] == "Time_input":
            user_input = st.time_input(
                label = f"Your {routines_infos['name']}",
            )

        btn_save_daily_stat = st.button(
            label = "Save",
            type = "primary",
            icon = ":material/check:"
        )

        if btn_save_daily_stat:
            if "daily_stats" not in st.session_state:
                st.session_state["daily_stats"] = []
            
            st.session_state.daily_stats.append({
                "name" : routines_infos["name"],
                "type" : routines_infos["type"],
                "value" : user_input
            })
            st.success(
                body="Your daily stat was saved!", 
                icon="🔥"
            )
    except Exception as e:
        st.error(
            body="An erreur has occured! {}".format(e), 
            icon="🚨"
        )

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