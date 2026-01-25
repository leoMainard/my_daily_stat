from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from my_daily_stat.config.enums import UserRole

@dataclass
class User:
    """Entité User - Représente un utilisateur dans le domaine métier"""
    
    firstname: str
    lastname: str
    email: str
    role: UserRole = UserRole.USER
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if not self.email or '@' not in self.email:
            raise ValueError("Email invalide")
        
        if not self.firstname or len(self.firstname) < 2:
            raise ValueError("Le prénom doit contenir au moins 2 caractères")
        
        if not self.lastname or len(self.lastname) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Factory method pour créer depuis un dict (DB)"""
        return cls(
            id=data.get('id'),
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            role=UserRole(data['role']),
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Conversion vers dict pour la DB"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def is_admin(self) -> bool:
        """Logique métier simple"""
        return self.role == UserRole.ADMIN

    def update_profile(self, firstname: Optional[str] = None, lastname: Optional[str] = None, email: Optional[str] = None):
        """Méthode métier pour mise à jour"""
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if email:
            self.email = email
        self.updated_at = datetime.now()