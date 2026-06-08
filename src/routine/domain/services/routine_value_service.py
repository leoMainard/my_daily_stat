from datetime import datetime
from typing import Any, Optional

from routine.db.repositories.routine_value_repository import RoutineValueRepository
from routine.domain.models.routine_value import RoutineValue


class RoutineValueService:
    def __init__(self, repo: RoutineValueRepository):
        self.repo = repo

    def save_routine_value(
        self,
        routine_id: int,
        value: Any,
        date: datetime
    ) -> RoutineValue:
        """
        Cette fonction enregistre une valeur de routine pour une date donnée.
        Si une valeur existe déjà pour cette routine et cette date, elle est mise à jour.
        """
        if not routine_id or not date:
            raise ValueError("Tous les champs sont obligatoires")
        
        try:
            routine_value_updated = self.repo.get_routine_value_by_routine_id_and_date(routine_id, date)
            if routine_value_updated:
                routine_value_updated.value = {"value": value}
                return self.repo.update(routine_value_updated)
        except Exception:
            raise Exception("Erreur lors de la mise à jour de votre routine")
        
        try:
            routine_value = RoutineValue(
                routine_id=routine_id,
                value={"value": value},
                date=date
            )
            return self.repo.create(routine_value)
        except Exception:
            raise Exception("Erreur lors de la sauvegarde de votre routine")

    def get_routine_value_by_routine_id_and_date(self, routine_id: int, date: datetime) -> Optional[RoutineValue]:
        """ Récupère une valeur de routine par sa date pour l'afficher dans l'interface utilisateur """
        try:
            routine_value = self.repo.get_routine_value_by_routine_id_and_date(routine_id, date)
            return routine_value
        except Exception:
            raise Exception("Erreur lors de la récupération de la valeur de votre routine")

    def delete_routine_value(self, routine_id: int, date: datetime):
        """ Pour une date donnée, il est possible de supprimer la valeur d'une routine (ex: si l'utilisateur s'est trompé) """
        # todo
        pass