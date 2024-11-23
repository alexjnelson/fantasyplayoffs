from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.fantasy_team import FantasyTeam

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    teams: List["FantasyTeam"] = Relationship(back_populates="user")