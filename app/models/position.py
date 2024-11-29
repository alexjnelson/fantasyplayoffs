from sqlmodel import SQLModel, Field
from typing import Optional

class Position(SQLModel, table=True):
    __tablename__ = "position"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str