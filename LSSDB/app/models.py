from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional

class Users(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="users_email_key"),
    )

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    email: str