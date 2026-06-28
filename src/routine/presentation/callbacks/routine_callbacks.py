import datetime
import time
import streamlit as st

from routine.db.adapters.postgres import get_cached_connection
from routine.db.repositories.routine_repository import RoutineRepository
from routine.db.repositories.routine_value_repository import RoutineValueRepository
from routine.domain.exceptions import (
    RoutineAlreadyExistsError,
    RoutineMissingOptionsError,
)
from routine.domain.services.routine_service import RoutineService
from routine.config.enums import RoutineType
from routine.domain.services.routine_value_service import RoutineValueService


def load_routines():
    service = RoutineService(RoutineRepository(get_cached_connection()))
    st.session_state.routines = [
        routine.to_dict()
        for routine in service.repo.find_all_by_user_id(st.session_state.user["id"])
    ]

    if len(st.session_state.routines) == 0:
        st.toast(
            body="Vous n'avez pas encore de routine. Cliquez sur le bouton + pour en ajouter une.",
            icon=":material/info:",
        )


@st.dialog("Edition d'une routine", on_dismiss="rerun")
def edition_routine(routine_infos: dict = None, type_dialog_routine="add"):
    """Fonction  de callback pour l'ajout, la modification ou la supression d'une routine.
    Le comportement de la fonction dépend du paramètre type qui peut être "add" ou "edit".

    En cas d'edition, passer les infos de la routine dans le paramètre routine_infos.
    """
    routine_name = st.text_input(
        label="Nom de la routine",
        value=routine_infos["name"] if routine_infos else "",
        placeholder="Exemple : Jogging du matin",
    )

    description = st.text_area(
        label="Description",
        value=routine_infos.get("description", "") if routine_infos else "",
        placeholder="Exemple : Suivre ma routine de jogging du matin pour rester en forme et améliorer ma santé cardiovasculaire.",
    )

    type = st.selectbox(
        label="Type",
        index=[
            index
            for index, r in enumerate(RoutineType)
            if r.name == routine_infos.get("type", "")
        ][0]
        if routine_infos is not None
        else 0,
        options=[r.value for r in RoutineType],
        help="Le type de la routine déterminera la manière dont vous pourrez interagir avec elle dans votre suivi quotidien. "
        "Par exemple, une routine de type Checkbox vous permettra de simplement cocher si vous avez réalisé la routine ou non, "
        "tandis qu'une routine de type Multiselect vous permettra de sélectionner plusieurs options pour suivre différents aspects de votre routine. "
        "Choisissez le type qui correspond le mieux à la nature de votre routine et à la manière dont vous souhaitez suivre vos progrès au fil du temps.",
    )

    if type_dialog_routine == "edit":
        st.info(
            body="Modifier le type supprimera l'historique de cette routine, soyez prudent !",
            icon=":material/info:",
        )

    multiselect_options = []
    if type == RoutineType.MULTISELECT.value:
        multiselect_options = st.multiselect(
            "Add options",
            options=routine_infos.get("multiselect_options", [])
            if routine_infos
            else [],
            default=routine_infos.get("multiselect_options", [])
            if routine_infos
            else [],
            placeholder="Ecrivez une option et appuyez sur Entrée pour l'ajouter",
            accept_new_options=True,
            help="Ajouter les différentes options que vous souhaitez suivre pour cette routine. Par exemple, si votre routine est 'Activités sportives', vous pourriez ajouter des options comme 'Football', 'Basketball', 'Natation', etc. **Les guillemets seront automatiquement supprimés pour éviter les problèmes de base de données.**",
        )

    left, right = st.columns([2, 1])

    btn_save_routine = left.button(
        label="Sauvegarder",
        type="primary",
        icon=":material/check:",
        use_container_width=True,
    )

    btn_delete_routine = right.button(
        label="Supprimer",
        type="secondary",
        icon=":material/delete:",
        help="Supprimer cette routine (toutes les données associées à cette routine seront également supprimées)",
        use_container_width=True,
    )

    if btn_save_routine:
        service = RoutineService(RoutineRepository(get_cached_connection()))
        try:
            if type_dialog_routine == "add":
                service.add_routine(
                    user_id=st.session_state.user["id"],
                    name=routine_name,
                    type=type,
                    multiselect_options=multiselect_options,
                    tags=[],
                    description=description,
                )

                st.success(body="Votre routine a été ajoutée !", icon="🔥")
            elif type_dialog_routine == "edit":
                service.update_routine(
                    routine_id=routine_infos["id"],
                    name=routine_name,
                    type=type,
                    multiselect_options=multiselect_options,
                    tags=[],
                    description=description,
                )
                st.success(body="Votre routine a été modifiée !", icon="🔥")
        except RoutineMissingOptionsError:
            st.warning(
                body="Les options sont obligatoires pour une routine de type Multiselect",
                icon="🚨",
            )
        except RoutineAlreadyExistsError:
            st.warning(
                body="Une routine existe déjà avec ce nom pour cet utilisateur",
                icon="🚨",
            )
        except Exception as e:
            st.error(body="Une erreur est survenue ... {}".format(e), icon="🚨")

    if btn_delete_routine:
        st.session_state["pending_delete_routine"] = routine_infos["id"]

    if (
        routine_infos
        and st.session_state.get("pending_delete_routine") == routine_infos["id"]
    ):
        # on affiche un message de confirmation avant de supprimer la routine
        st.warning("Êtes-vous sûr de vouloir supprimer cette routine ?", icon="⚠️")
        col1, col2 = st.columns([2, 1])
        btn_confirm_delete = col1.button(
            label="Confirmer la suppression",
            type="primary",
            use_container_width=True,
            icon=":material/delete:",
        )

        btn_cancel_delete = col2.button(
            label="Annuler",
            type="secondary",
            icon=":material/close:",
            use_container_width=True,
            on_click=lambda: st.session_state.pop("pending_delete_routine", None),
        )

        if btn_confirm_delete:
            service = RoutineService(RoutineRepository(get_cached_connection()))
            service.delete_routine(routine_infos["id"])
            del st.session_state["pending_delete_routine"]
            st.success(body="Votre routine a été supprimée !", icon="🔥")
            with st.spinner("Ce module se fermera dans quelques instants ..."):
                time.sleep(2)
                st.switch_page("pages/routine.py")

        if btn_cancel_delete:
            del st.session_state["pending_delete_routine"]


def display_routine(routines_infos: dict, date_value: datetime.date = None):
    @st.dialog(routines_infos["name"], on_dismiss="rerun")
    def _dialog():
        @st.fragment
        def _content():
            try:
                service = RoutineValueService(
                    RoutineValueRepository(get_cached_connection())
                )

                st.badge(
                    routines_infos.get("description", ""),
                    icon=":material/lightbulb_2:",
                    color="blue",
                )

                routine_id = routines_infos["id"]

                # Incrémenter ce compteur force la recréation des widgets (nouvelle clé = nouvelle instance)
                widget_version = st.session_state.get(f"wv_{routine_id}", 0)

                # Empêche le date_input de s'ouvrir automatiquement au focus
                st.markdown(
                    '<div style="height:0;overflow:hidden"><input autofocus /></div>',
                    unsafe_allow_html=True,
                )

                routine_date_value: datetime.date = st.date_input(
                    label="Date de suivi pour votre routine",
                    value=date_value if date_value else "today",
                    format="DD/MM/YYYY",
                    key=f"date_{routine_id}",
                )

                routine_value = service.get_routine_value_by_routine_id_and_date(
                    routine_id, routine_date_value
                )

                date_key = str(routine_date_value)
                wk = f"{routine_id}_{date_key}_v{widget_version}"

                if routines_infos["type"] == RoutineType.TEXT.name:
                    user_input = st.text_area(
                        label=f"text_{routines_infos['name']}",
                        placeholder="Ajoutez votre texte ici.",
                        label_visibility="collapsed",
                        value=routine_value.value["value"] if routine_value else "",
                        key=f"text_{wk}",
                    )

                elif routines_infos["type"] == RoutineType.CHECKBOX.name:
                    user_input = st.checkbox(
                        label="Cliquez ici si vous avez réalisé votre routine aujourd'hui !",
                        value=bool(routine_value.value["value"])
                        if routine_value
                        else False,
                        key=f"checkbox_{wk}",
                    )

                elif routines_infos["type"] == RoutineType.FEEDBACK.name:
                    feedback_key = f"feedback_{wk}"
                    if routine_value and feedback_key not in st.session_state:
                        st.session_state[feedback_key] = routine_value.value["value"]
                    user_input = st.feedback(options="faces", key=feedback_key)

                elif routines_infos["type"] == RoutineType.MULTISELECT.name:
                    user_input = st.multiselect(
                        label=f"multiselect_{routines_infos['name']}",
                        options=routines_infos.get("multiselect_options", []),
                        placeholder="Sélectionnez vos options ici.",
                        label_visibility="collapsed",
                        default=routine_value.value["value"] if routine_value else [],
                        key=f"multiselect_{wk}",
                    )

                elif routines_infos["type"] == RoutineType.NUMBER.name:
                    user_input = st.number_input(
                        label=f"number_{routines_infos['name']}",
                        placeholder="Ajoutez votre nombre ici.",
                        step=1,
                        label_visibility="collapsed",
                        value=routine_value.value["value"] if routine_value else None,
                        key=f"number_{wk}",
                    )

                elif routines_infos["type"] == RoutineType.TIME.name:
                    time_value = None
                    if routine_value:
                        raw = routine_value.value["value"]
                        time_value = (
                            datetime.time.fromisoformat(raw)
                            if isinstance(raw, str)
                            else raw
                        )
                    user_input = st.time_input(
                        label=f"time_{routines_infos['name']}",
                        label_visibility="collapsed",
                        value=time_value,
                        key=f"time_{wk}",
                    )

                left, center, right = st.columns(3)
                btn_save_routine = left.button(
                    label="Sauvegarder",
                    type="primary",
                    icon=":material/check:",
                    help="Sauvegarder la valeur de cette routine pour la date sélectionnée",
                    use_container_width=True,
                )

                btn_edit_routine = center.button(
                    label="Modifier",
                    type="secondary",
                    icon=":material/edit:",
                    help="Modifier les informations de cette routine (nom, description, type, etc.)",
                    use_container_width=True,
                )

                btn_delete_routine = right.button(
                    label="Supprimer",
                    type="secondary",
                    help="Supprimer la valeur de cette routine pour la date sélectionnée",
                    icon=":material/delete:",
                    use_container_width=True,
                )

                if btn_save_routine:
                    try:
                        service.save_routine_value(
                            routine_id=routine_id,
                            value=user_input,
                            date=routine_date_value,
                        )
                        st.success(body="Valeur sauvegardée !", icon="🔥")
                        with st.spinner(
                            "Ce module se fermera dans quelques instants ..."
                        ):
                            time.sleep(1)
                            st.switch_page("pages/routine.py")
                    except Exception as e:
                        st.error(body=str(e), icon="🚨")

                if btn_edit_routine:
                    st.session_state["pending_edit_routine"] = routines_infos
                    st.rerun()

                if btn_delete_routine:
                    st.session_state["pending_delete_routine_value"] = routine_id

                if st.session_state.get("pending_delete_routine_value") == routine_id:
                    # on affiche un message de confirmation avant de supprimer la valeur de la routine
                    st.warning(
                        "Êtes-vous sûr de vouloir supprimer cette valeur ?", icon="⚠️"
                    )
                    col1, col2 = st.columns([2, 1])
                    btn_confirm_delete = col1.button(
                        label="Confirmer la suppression",
                        type="primary",
                        use_container_width=True,
                        icon=":material/delete:",
                    )

                    btn_cancel_delete = col2.button(
                        label="Annuler",
                        type="secondary",
                        icon=":material/close:",
                        use_container_width=True,
                        on_click=lambda: st.session_state.pop(
                            "pending_delete_routine_value", None
                        ),
                    )

                    if btn_confirm_delete:
                        try:
                            service.delete_routine_value(
                                routine_id=routine_id, date=routine_date_value
                            )
                            del st.session_state["pending_delete_routine_value"]
                        except Exception as e:
                            st.error(body=str(e), icon="🚨")
                            return
                        st.session_state[f"wv_{routine_id}"] = widget_version + 1
                        st.toast("Votre valeur de routine a été supprimée !", icon="🔥")
                        st.rerun(scope="fragment")

                    if btn_cancel_delete:
                        del st.session_state["pending_delete_routine_value"]
            except Exception as e:
                st.error(body="Une erreur est survenue ... {}".format(e), icon="🚨")

        _content()

    _dialog()
