import streamlit as st

@st.dialog("New routine")
def add_routine():
    try:
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
            options = ("Text", "Checkbox","Feedback","Multiselect", "Number input", "Time_input")
        )

        multiselect_options = []
        if type == "Multiselect":
            multiselect_options = st.multiselect(
                "Add options", 
                options = ("Example : Football"), 
                accept_new_options=True
            )

        btn_save_add_routine = st.button(
            label = "Save",
            type = "primary",
            icon = ":material/check:"
        )

        if btn_save_add_routine:
            if not routine_name:
                st.warning('You have to add a name.', icon="⚠️")

            elif not type:
                st.warning('You have to chose a type.', icon="⚠️")

            elif type == "Multiselect" and not multiselect_options:
                st.warning('You have to add options.', icon="⚠️")
            else:
                if "routines" not in st.session_state:
                    st.session_state["routines"] = []
                
                st.session_state.routines.append({
                    "name" : routine_name,
                    "type" : type,
                    "description": description,
                    "multiselect_option" : multiselect_options
                })
                st.success(
                    body="Votre routine a été ajoutée !", 
                    icon="🔥"
                )
                st.rerun()
    except Exception as e:
        st.error(
            body="An erreur has occured! {}".format(e), 
            icon="🚨"
        )

@st.dialog("Daily routine")
def display_routine(routines_infos: dict):
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