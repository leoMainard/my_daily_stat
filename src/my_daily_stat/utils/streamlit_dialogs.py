import streamlit as st

@st.dialog("New stat")
def add_stat():
    try:
        stat_name = st.text_input(
            label = "Stat name",
            placeholder = "Example : Sport"
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

        btn_save_add_stat = st.button(
            label = "Save",
            type = "primary",
            icon = ":material/check:"
        )

        if btn_save_add_stat:
            if not stat_name:
                st.warning('You have to add a name.', icon="⚠️")

            elif not type:
                st.warning('You have to chose a type.', icon="⚠️")

            elif type == "Multiselect" and not multiselect_options:
                st.warning('You have to add options.', icon="⚠️")
            else:
                if "stat" not in st.session_state:
                    st.session_state["stat"] = []
                
                st.session_state.stat.append({
                    "name" : stat_name,
                    "type" : type,
                    "multiselect_option" : multiselect_options
                })
                st.success(
                    body="Your stat was saved!", 
                    icon="🔥"
                )
                st.rerun()
    except Exception as e:
        st.error(
            body="An erreur has occured! {}".format(e), 
            icon="🚨"
        )

@st.dialog("Daily stat")
def display_stat(stats_infos: dict):
    try:
        st.write(f"## {stats_infos['name']}")

        st.date_input(
            label = "Date",
            value = "today",
            key = "selected_date"
        )

        if stats_infos["type"] == "Text":
            user_input = st.text_input(
                label = f"Your {stats_infos['name']}",
                placeholder = f"Example : I did 30 minutes of sport"
            )

        elif stats_infos["type"] == "Checkbox":
            user_input = st.checkbox(
                label = f"Did you {stats_infos['name']} today ?"
            )

        elif stats_infos["type"] == "Feedback":
            user_input = st.feedback(
                options = "faces"
            )

        elif stats_infos["type"] == "Multiselect":
            user_input = st.multiselect(
                label = f"Select your {stats_infos['name']} today",
                options = stats_infos.get("multiselect_option", [])
            )

        elif stats_infos["type"] == "Number input":
            user_input = st.number_input(
                label = f"Your {stats_infos['name']}",
                step=1
            )

        elif stats_infos["type"] == "Time_input":
            user_input = st.time_input(
                label = f"Your {stats_infos['name']}",
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
                "name" : stats_infos["name"],
                "type" : stats_infos["type"],
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