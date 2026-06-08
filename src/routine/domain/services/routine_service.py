from routine.db.repositories.routine_repository import RoutineRepository
from routine.domain.models.routine import Routine
from routine.config.enums import RoutineType
from typing import Optional, List, Union
from routine.domain.exceptions import RoutineAlreadyExistsError, RoutineMissingOptionsError

class RoutineService:
    def __init__(self, repo: RoutineRepository):
        self.repo = repo

    def add_routine(
        self,
        user_id: int,
        name: str,
        type: Union[str, RoutineType],
        multiselect_options: Optional[List[str]],
        tags: list,
        description: str,
    ) -> Routine:
        if not user_id or not name or not type:
            raise ValueError("Tous les champs sont obligatoires")
        
        # Normalisation de type pour accepter à la fois des chaînes de caractères et des enums
        if isinstance(type, str):
            try:
                type = RoutineType(type).name
            except ValueError:
                pass
        
        if type == RoutineType.MULTISELECT.name and not multiselect_options:
            raise RoutineMissingOptionsError("Les options sont obligatoires pour une routine de type Multiselect")

        if self.repo.find_by_user_id_and_name(user_id, name):
            raise RoutineAlreadyExistsError("Une routine existe déjà avec ce nom pour cet utilisateur")
        
        # Suppression des '"' dans les options du multiselect pour éviter les problèmes de parsing JSON
        if multiselect_options:
            multiselect_options = [option.replace('"', ' ') for option in multiselect_options]
            
        routine = Routine(
            user_id=user_id,
            name=name,
            type=type,
            multiselect_options=multiselect_options or [],
            tags=tags,
            description=description,
        )
        return self.repo.create(routine)
    
    def update_routine(self, routine_id: int, name: str, type: Union[str, RoutineType], multiselect_options: Optional[List[str]], tags: list, description: str) -> Routine:
        routine = self.repo.find_by_id(routine_id)
        if not routine:
            raise ValueError("Routine non trouvée")
        
        # Normalisation de type pour accepter à la fois des chaînes de caractères et des enums
        if isinstance(type, str):
            try:
                type = RoutineType(type).name
            except ValueError:
                pass
        
        if type == RoutineType.MULTISELECT.name and not multiselect_options:
            raise RoutineMissingOptionsError("Les options sont obligatoires pour une routine de type Multiselect")

        existing_routine = self.repo.find_by_user_id_and_name(routine.user_id, name)
        if existing_routine and existing_routine.id != routine_id:
            raise RoutineAlreadyExistsError("Une routine existe déjà avec ce nom pour cet utilisateur")
        
        # Suppression des '"' dans les options du multiselect pour éviter les problèmes de parsing JSON
        if multiselect_options:
            multiselect_options = [option.replace('"', ' ') for option in multiselect_options]

        routine.update(
            name=name,
            type=type,
            multiselect_options=multiselect_options or [],
            tags=tags,
            description=description
        )
        return self.repo.update(routine)
        
    def delete_routine(self, routine_id: int):
        routine = self.repo.find_by_id(routine_id)
        if not routine:
            raise ValueError("Routine non trouvée")
        return self.repo.delete(routine_id)