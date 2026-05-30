from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import bcrypt
from routine.config.enums import UserRole

@dataclass
class User:
    """Entité User - Représente un utilisateur dans le domaine métier"""

    firstname: str
    lastname: str
    email: str
    password_hash: str = ""
    role: UserRole = UserRole.USER
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.email or '@' not in self.email:
            raise ValueError("Email invalide")
        if not self.firstname or len(self.firstname) < 2:
            raise ValueError("Le prénom doit contenir au moins 2 caractères")
        if not self.lastname or len(self.lastname) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")

    def set_password(self, plain_password: str) -> None:
        self.password_hash = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.password_hash.encode())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Factory method pour créer depuis un dict (DB)"""
        return cls(
            id=data.get('id'),
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            password_hash=data.get('password_hash', ''),
            role=UserRole(data['role']),
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Conversion vers dict pour la DB"""
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def is_admin(self) -> bool:
        """Logique métier simple"""
        return self.role == UserRole.ADMIN

    def update(self, **kwargs) -> None:
        """Met à jour les champs de l'utilisateur et la date de mise à jour"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()