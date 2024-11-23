from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.fantasy_team import FantasyTeam

class League(SQLModel, table=True):
    __tablename__ = "league"
    id: Optional[int] = Field(default=None, primary_key=True)
    commissioner_id: int = Field(foreign_key="user.id")
    name: str
    fantasy_teams: List["FantasyTeam"] = Relationship(back_populates="league")
