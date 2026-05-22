from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from contextlib import contextmanager

T = TypeVar('T')

class DatabaseAdapter(ABC):
    """Interface abstraite pour les adaptateurs de base de données"""
    
    @abstractmethod
    def connect(self) -> None:
        """Établit la connexion"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Ferme la connexion"""
        pass
    
    @abstractmethod
    @contextmanager
    def transaction(self):
        """Context manager pour les transactions"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Exécute une requête SELECT"""
        pass
    
    @abstractmethod
    def execute_command(self, command: str, params: Optional[Dict] = None) -> int:
        """Exécute INSERT/UPDATE/DELETE, retourne le nombre de lignes affectées"""
        pass 


class Repository(ABC, Generic[T]):
    """Interface de base pour les repositories"""
    
    def __init__(self, db_adapter: DatabaseAdapter):
        self.db = db_adapter
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass