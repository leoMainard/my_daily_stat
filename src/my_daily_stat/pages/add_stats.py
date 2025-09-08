import streamlit as st

from my_daily_stat.utils.streamlit_dialogs import add_stat

st.write("# Welcome to My Daily Stat! 👋")



btn_add_stat = st.button(
    label = "**\+**",
    type = "primary"
)


if btn_add_stat:
    result_add_stat = add_stat()
    if result_add_stat:
        st.toast("Your stat was saved!", icon="😍")
    else:
        st.toast("An erreur has occured!", icon="🚨")

# boucle pour charger tous les boutons d'affichage de stat