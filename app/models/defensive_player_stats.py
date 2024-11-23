from sqlmodel import SQLModel, Field

class DefensivePlayerStats(SQLModel, table=True):
    __tablename__ = "defensive_player_stats"
    game_id: int = Field(foreign_key="nfl_player_game.id")
    def_tds: float
    def_pts: float
    def_xp_ret_two_pt_conv: float
    ints: float
    sacks: float
    fumble_rec: float
    pts_against_0: float
    pts_against_1_14: float
    pts_against_15_21: float
    pts_against_22_28: float
    pts_against_29_35: float
    pts_against_35_plus: float
