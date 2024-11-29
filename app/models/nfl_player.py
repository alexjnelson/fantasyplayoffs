from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class NFLPlayer(SQLModel, table=True):
    __tablename__ = "nfl_player"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    photo_url: str
    nfl_team_id: int = Field(foreign_key="nfl_team.id")
    position_id: int = Field(foreign_key="position.id")
    games: Optional[List["NFLPlayerGame"]] = Relationship(back_populates="nfl_player")
