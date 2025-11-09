from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import DateTime

class User(SQLModel, table=True):

    __tablename__ = "user"

    user_id: int | None = Field(default=None, primary_key=True)
    nom: str = Field(sa_column=Column(String(100), nullable=False))
    prenom: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    password: str = Field(sa_column=Column(String, nullable=False))
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=lambda: datetime.now(timezone.utc))
)

    # Relation avec StatObject
    stat_objects: List["StatObject"] = Relationship(back_populates="user")

class StatObject(SQLModel, table=True):

    __tablename__ = "statobject"

    statobject_id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id", nullable=False)
    type: str = Field(sa_column=Column(String(50), nullable=False))
    name: str = Field(sa_column=Column(String(100), nullable=False))
    description: Optional[str] = Field(sa_column=Column(String(255), nullable=True))
    options: dict | None = Field(sa_column=Column(JSONB, nullable=True))
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=lambda: datetime.now(timezone.utc))
    )

    # Relations bidirectionnelles
    user: Optional[User] = Relationship(back_populates="stat_objects")
    historic_stats: List["HistoricStats"] = Relationship(back_populates="stat_object")

class HistoricStats(SQLModel, table=True):
    __tablename__ = "historicstats"

    historicstat_id: int | None = Field(default=None, primary_key=True)
    statobject_id: int = Field(foreign_key="statobject.statobject_id", nullable=False)
    date: datetime = Field(nullable=False)
    value: str = Field(nullable=False)
   
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relation avec StatObject
    stat_object: Optional[StatObject] = Relationship(back_populates="historic_stats")