import streamlit as st

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.routine_repository import RoutineRepository
from routine.domain.exceptions import RoutineAlreadyExistsError, RoutineMissingOptionsError
from routine.domain.services.routine_service import RoutineService
from routine.config.enums import RoutineType

def load_routines():
    service = RoutineService(RoutineRepository(get_cached_connection()))
    st.session_state.routines = [routine.to_dict() for routine in service.repo.find_all_by_user_id(st.session_state.user["id"])]
    
    if len(st.session_state.routines) == 0:
        st.toast(
            body="Vous n'avez pas encore de routine. Cliquez sur le bouton + pour en ajouter une.", 
            icon=":material/info:"
        )

@st.dialog("Edition d'une routine", on_dismiss="rerun")
def edition_routine(routine_infos: dict = None, type = "add"):
    """ Fonction  de callback pour l'ajout, la modification ou la supression d'une routine.
    Le comportement de la fonction dépend du paramètre type qui peut être "add", "edit" ou "delete".

    En cas d'edition ou de suppression, passer les infos de la routine dans le paramètre routine_infos.
    """
    routine_name = st.text_input(
        label = "Nom de la routine",
        value = routine_infos["name"] if routine_infos else "",
        placeholder = "Exemple : Jogging du matin"
    )

    description = st.text_area(
        label = "Description",
        value = routine_infos.get("description", "") if routine_infos else "",
        placeholder = "Exemple : Suivre ma routine de jogging du matin pour rester en forme et améliorer ma santé cardiovasculaire."
    )

    type = st.selectbox(
        label = "Type",
        index = [index for index, r in enumerate(RoutineType) if r.name == routine_infos.get("type", "")][0] if routine_infos is not None else 0,
        options = [r.value for r in RoutineType]
    )

    multiselect_options = []
    if type == RoutineType.MULTISELECT.value :
        multiselect_options = st.multiselect(
            "Add options", 
            options = routine_infos.get("multiselect_options", []) if routine_infos else [],
            default = routine_infos.get("multiselect_options", []) if routine_infos else [],
            placeholder = "Ecrivez une option et appuyez sur Entrée pour l'ajouter",
            accept_new_options=True,
            help="Ajouter les différentes options que vous souhaitez suivre pour cette routine. Par exemple, si votre routine est 'Activités sportives', vous pourriez ajouter des options comme 'Football', 'Basketball', 'Natation', etc. **Les guillemets seront automatiquement supprimés pour éviter les problèmes de base de données.**"
        )

    btn_save_routine = st.button(
        label = "Sauvegarder",
        type = "primary",
        icon = ":material/check:"
    )

    if btn_save_routine:
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

def display_routine(routines_infos: dict):
    @st.dialog(routines_infos["name"], on_dismiss="rerun")
    def _dialog():
        try:
            st.badge(routines_infos.get("description", ""), icon=":material/lightbulb_2:" ,color="blue")

            if routines_infos["type"] == RoutineType.TEXT.name:
                user_input = st.text_input(
                    label = f"text_{routines_infos['name']}",
                    placeholder = f"Ajoutez votre texte ici.",
                    label_visibility="collapsed"
                )

            elif routines_infos["type"] == RoutineType.CHECKBOX.name:
                user_input = st.checkbox(
                    label = f"Cliquez ici si vous avez réalisé votre routine aujourd'hui !"
                )

            elif routines_infos["type"] == RoutineType.FEEDBACK.name:
                user_input = st.feedback(
                    options = "faces"
                )

            elif routines_infos["type"] == RoutineType.MULTISELECT.name:
                user_input = st.multiselect(
                    label = f"multiselect_{routines_infos['name']}",
                    options = routines_infos.get("multiselect_options", []),
                    placeholder = f"Sélectionnez vos options ici.",
                    label_visibility="collapsed"
                )

            elif routines_infos["type"] == RoutineType.NUMBER.name:
                user_input = st.number_input(
                    label = f"number_{routines_infos['name']}",
                    placeholder = f"Ajoutez votre nombre ici.",
                    step=1,
                    label_visibility="collapsed"
                )

            elif routines_infos["type"] == RoutineType.TIME.name:
                user_input = st.time_input(
                    label = f"time_{routines_infos['name']}",
                    label_visibility="collapsed"
                )

            left, mid, right = st.columns(3)
            btn_save_routine = left.button(
                label = "Sauvegarder",
                type = "primary",
                icon = ":material/check:",
                use_container_width=True
            )

            btn_edit_routine = mid.button(
                label = "Modifier",
                type = "secondary",
                icon = ":material/edit:",
                use_container_width=True
            )

            btn_delete_routine = right.button(
                label = "Supprimer",
                type = "secondary",
                icon = ":material/delete:",
                use_container_width=True
            )

            if btn_save_routine:
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
            
            if btn_edit_routine:
                # on met en attente les infos de la routine à éditer dans le session state pour les récupérer dans le dialog d'édition
                st.session_state["pending_edit_routine"] = routines_infos
                st.rerun()
        except Exception as e:
            st.error(
                body="An erreur has occured! {}".format(e),
                icon="🚨"
            )

    _dialog()