from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class RosterSettings(SQLModel, table=True):
    __tablename__ = "roster_settings"
    league_id: int = Field(foreign_key="league.id")
    qb: int
    rb: int
    wr: int
    te: int
    pk: int
