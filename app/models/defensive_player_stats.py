from sqlmodel import SQLModel, Field

class DefensivePlayerStats(SQLModel, table=True):
    __tablename__ = "defensive_player_stats"
    game_id: int = Field(foreign_key="nfl_player_game.id", primary_key=True)
    def_tds: float
    def_xp_ret_two_pt_conv: float
    ints: float
    sacks: float
    fumble_rec: float
    pts_against_0: float
    pts_against_1_6: float
    pts_against_7_13: float
    pts_against_14_20: float
    pts_against_21_27: float
    pts_against_28_34: float
    pts_against_35_plus: float
