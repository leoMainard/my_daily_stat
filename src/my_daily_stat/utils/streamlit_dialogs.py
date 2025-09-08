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
def display_stat():
    pass