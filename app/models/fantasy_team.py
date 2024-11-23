from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.RosterSlot import RosterSlot

class FantasyTeam(SQLModel, table=True):
    __tablename__ = "fantasy_team"
    id: Optional[int] = Field(default=None, primary_key=True)
    league_id: int = Field(foreign_key="league.id")
    team_name: str
    roster_slots: List["RosterSlot"] = Relationship(back_populates="fantasy_team")
