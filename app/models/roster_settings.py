from sqlmodel import SQLModel, Field

class RosterSettings(SQLModel, table=True):
    __tablename__ = "roster_settings"
    league_id: int = Field(foreign_key="league.id", primary_key=True)
    qb: int
    rb: int
    wr: int
    te: int
    pk: int
    dst: int
