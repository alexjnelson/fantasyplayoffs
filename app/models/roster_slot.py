from sqlmodel import SQLModel, Field, Relationship

class RosterSlot(SQLModel, table=True):
    __tablename__ = "roster_slot"
    fantasy_team_id: int = Field(foreign_key="fantasy_team.id")
    week_no: int
    nfl_player_id: int = Field(foreign_key="nfl_player.id")
