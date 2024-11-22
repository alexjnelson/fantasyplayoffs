from sqlmodel import SQLModel, Field

class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field()
    email: str = Field(index=True, unique=True)
