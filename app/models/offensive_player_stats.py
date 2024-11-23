from sqlmodel import SQLModel, Field

class OffensivePlayerStats(SQLModel, table=True):
    __tablename__ = "offensive_player_stats"
    game_id: int = Field(foreign_key="nfl_player_game.id")
    pass_tds: float
    pass_tds: float
    rush_tds: float
    rush_Tsds: float
    pass_two_pt_conv: float
    rush_two_pt_conv: float
    rec_tds: float
    rec_yds: float
    rec_two_pt_conv: float
    other_tds: float
    fumbles: float
