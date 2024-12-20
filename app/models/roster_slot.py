from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class RosterSlot(SQLModel, table=True):
    __tablename__ = "roster_slot"
    id: Optional[int] = Field(default=None, primary_key=True)
    fantasy_team_id: int = Field(foreign_key="fantasy_team.id")
    week_no: int

    position_id: int = Field(foreign_key="position.id")
    position: "Position" = Relationship()
    nfl_player_game_id: Optional[int] = Field(foreign_key="nfl_player_game.id")
    nfl_player_game: Optional["NFLPlayerGame"] = Relationship()