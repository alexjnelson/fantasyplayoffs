from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class FantasyTeam(SQLModel, table=True):
    __tablename__ = "fantasy_team"
    id: Optional[int] = Field(default=None, primary_key=True)
    league_id: int = Field(foreign_key="league.id")
    user_id: int = Field(foreign_key="users.id")    
    team_name: str
    league: "League" = Relationship(back_populates="fantasy_teams")
    user: "User" = Relationship(back_populates="teams")
    roster_slots: Optional[List["RosterSlot"]] = Relationship()
