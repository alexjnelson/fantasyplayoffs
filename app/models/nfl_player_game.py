from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


from app.models.nfl_player import NFLPlayer

class NFLPlayerGame(SQLModel, table=True):
    __tablename__ = "nfl_player_game"
    id: Optional[int] = Field(default=None, primary_key=True)
    week_no: int
    start_time: datetime
    is_home: bool
    opponent_id: int = Field(foreign_key="nfl_team.id")
    player_id: int = Field(foreign_key="nfl_player.id")
    nfl_player: "NFLPlayer" = Relationship(back_populates="games")