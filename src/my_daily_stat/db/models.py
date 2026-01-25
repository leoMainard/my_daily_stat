from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class UserModel(Base):
    """
    Model SQLAlchemy - représente la structure de la table
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(String(50), nullable=False, server_default='user')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())


class UserStatsModel(Base):
    __tablename__ = 'user_stats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    login_count = Column(Integer, nullable=False, server_default='0')
    posts_count = Column(Integer, nullable=False, server_default='0')
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

# TODO