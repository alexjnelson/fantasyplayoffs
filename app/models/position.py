from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Position(SQLModel, table=True):
    __tablename__ = "position"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str