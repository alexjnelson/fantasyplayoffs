from sqlmodel import SQLModel, Field

class OffensivePlayerStats(SQLModel, table=True):
    __tablename__ = "offensive_player_stats"
    game_id: int = Field(foreign_key="nfl_player_game.id", primary_key=True)
    pass_tds: float
    pass_yds: float
    pass_cmp: float
    pass_att: float
    pass_two_pt_conv: float
    rush_tds: float
    rush_att: float
    rush_yds: float
    rush_two_pt_conv: float
    targets: float
    recs: float
    rec_tds: float
    rec_yds: float
    rec_two_pt_conv: float
    other_tds: float
    fumbles: float
