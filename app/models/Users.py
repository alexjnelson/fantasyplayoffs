from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="users_email_key"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    teams: Optional[List["FantasyTeam"]] = Relationship(back_populates="user")  
