from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from . import PersonInfo

#Модель почт людей связанная с Информацией о Людях
class PersonMail(SQLModel, table=True):
    __tablename__ = "PersonMail"

    Id: Optional[int] = Field(default=None, primary_key=True)
    Mail: str = Field(index=True, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    PersonInfoId: int = Field(foreign_key="PersonInfo.Id")
    person: "PersonInfo" = Relationship(back_populates="emails")