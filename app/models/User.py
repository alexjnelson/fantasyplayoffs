from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
