from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from routine.config.enums import RoutineType

@dataclass
class Routine:
    """ Classe représentant une routine journalière."""
    user_id: int
    type: RoutineType
    name: str
    id: Optional[int] = None
    multiselect_options: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Le nom de la routine est obligatoire")
        if not self.type:
            raise ValueError("Le type de la routine est obligatoire")
        if self.type == RoutineType.MULTISELECT.name and not self.multiselect_options:
            raise ValueError("Les options sont obligatoires pour une routine de type Multiselect")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Routine':
        """ Factory method pour créer une Routine depuis un dict (ex: DB) """
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            name=data.get('name', ''),
            type=data['type'],
            multiselect_options=data.get('multiselect_options', []),
            tags=data.get('tags', []),
            description=data.get('description', ''),
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> dict:
        """ Convertit l'instance en dict pour la DB """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'multiselect_options': self.multiselect_options,
            'tags': self.tags,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, **kwargs) -> None:
        """ Met à jour les champs de la routine et la date de mise à jour """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
