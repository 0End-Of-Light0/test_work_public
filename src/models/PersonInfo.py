from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from . import PersonMail

class PersonInfo(SQLModel, table=True):
    __tablename__ = "PersonInfo"

    Id: Optional[int] = Field(default=None, primary_key=True)
    NameSurnamePatronymic: str = Field(
        index=True,
        unique=True,
        min_length=2,
        max_length=100,
        description="Full name in format 'Lastname Firstname Middlename'"
    )
    Gender: Optional[str] = None
    Nationality: Optional[str] = None
    Age: Optional[int] = Field(None, ge=0, le=150)
    emails: List["PersonMail"] = Relationship(back_populates="person")

