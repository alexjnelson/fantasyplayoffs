from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
from typing import Optional, List

class Users(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="users_email_key"),
    )

    id: str = Field(default=None, primary_key=True)
    name: str
    email: str
    teams: Optional[List["FantasyTeam"]] = Relationship()
