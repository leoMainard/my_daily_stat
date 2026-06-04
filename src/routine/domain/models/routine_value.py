
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class RoutineValue():
    """ Classe représentant une valeur de routine journalière. """
    routine_id : int
    value : dict
    id: int = None
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.routine_id:
            raise ValueError("L'id de la routine est obligatoire")
        if not self.value:
            raise ValueError("La valeur de la routine est obligatoire. Ajoutez {'type': 'valeur'}")
        
    @classmethod
    def from_dict(cls, data: dict) -> 'RoutineValue':
        """ Factory method pour créer une RoutineValue depuis un dict (ex: DB) """
        return cls(
            id=data.get('id'),
            routine_id=data['routine_id'],
            value=data['value'],
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> dict:
        """ Convertit l'instance en dict pour la DB """
        return {
            'id': self.id,
            'routine_id': self.routine_id,
            'value': self.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, **kwargs) -> None:
        """ Met à jour les champs de la routine value et la date de mise à jour """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()