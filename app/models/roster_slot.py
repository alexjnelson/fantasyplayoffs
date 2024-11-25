from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.models.nfl_player import NFLPlayer
from app.models.nfl_player_game import NFLPlayerGame

class RosterSlot(SQLModel, table=True):
    __tablename__ = "roster_slot"
    id: Optional[int] = Field(default=None, primary_key=True)
    fantasy_team_id: int = Field(foreign_key="fantasy_team.id")
    week_no: int
    position_id: int = Field(foreign_key="position")
    nfl_player_game_id: int = Field(foreign_key="nfl_player_game.id")
    nfl_player_game: "NFLPlayerGame" = Relationship()