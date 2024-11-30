from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class League(SQLModel, table=True):
    __tablename__ = "league"
    id: Optional[int] = Field(default=None, primary_key=True)
    commissioner_id: str = Field(foreign_key="users.id")
    name: str
    fantasy_teams: Optional[List["FantasyTeam"]] = Relationship(back_populates="league")
    roster_settings: Optional["RosterSettings"] = Relationship(sa_relationship_kwargs={"uselist": False})
    scoring_settings: Optional["ScoringSettings"] = Relationship(sa_relationship_kwargs={"uselist": False})