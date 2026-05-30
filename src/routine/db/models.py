from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from routine.config.enums import UserRole, RoutineType

Base = declarative_base()

class UserModel(Base):
    """
    Model SQLAlchemy - représente la structure de la table
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False, server_default='USER')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

class RoutinesModel(Base):
    __tablename__ = 'routines'
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_routine_user_id_name'), # Assure qu'un même utilisateur ne peut pas avoir deux routines avec le même nom
    )
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum(RoutineType, name="routine_type"), nullable=False, server_default='TEXT')
    multiselect_options = Column(JSON, nullable=True, server_default='[]') # option dans le cas d'une routine de type multiselect
    tags = Column(JSON, nullable=True, server_default='[]')
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

class RoutineValuesModel(Base):
    __tablename__ = 'routine_values'
    
    id = Column(Integer, primary_key=True)
    routine_id = Column(Integer, ForeignKey('routines.id', ondelete='CASCADE'), nullable=False)
    value = Column(JSONB, nullable=False)
    recorded_at = Column(DateTime, nullable=False, server_default=func.now())

# TODO