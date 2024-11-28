from sqlmodel import SQLModel, Field

class ScoringSettings(SQLModel, table=True):
    __tablename__ = "scoring_settings"
    league_id: int = Field(foreign_key="league.id", primary_key=True)
    # Offensive scoring settings
    pass_tds: float
    pass_yds: float
    rush_tds: float
    rush_yds: float
    pass_two_pt_conv: float
    rush_two_pt_conv: float
    rec_tds: float
    rec_yds: float
    rec_two_pt_conv: float
    other_tds: float
    fumbles: float
    # Defensive scoring settings
    def_tds: float
    def_pts: float
    xp_ret_two_pt_conv: float
    ints: float
    sacks: float
    fumble_rec: float
    pts_against_0: float
    pts_against_1_14: float
    pts_against_15_21: float
    pts_against_22_28: float
    pts_against_29_35: float
    pts_against_35_plus: float
    # Kicker scoring settings
    fg: float
    fg_40: float
    fg_50: float
    xp: float
