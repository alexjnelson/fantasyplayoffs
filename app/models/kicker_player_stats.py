from sqlmodel import SQLModel, Field

class KickerPlayerStats(SQLModel, table=True):
    __tablename__ = "kicker_player_stats"
    game_id: int = Field(foreign_key="nfl_player_game.id")
    fg: float
    fg_40: float
    fg_50: float
    xp: float
