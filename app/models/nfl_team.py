from sqlmodel import SQLModel, Field
from typing import Optional

class NFLTeam(SQLModel, table=True):
    __tablename__ = "nfl_team"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    logo_url: str
