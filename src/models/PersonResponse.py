from sqlmodel import SQLModel
from typing import List, Optional

class PersonResponse(SQLModel):
    Id: int
    NameSurnamePatronymic: str
    Gender: Optional[str] = None
    Nationality: Optional[str] = None
    Age: Optional[int] = None
    emails: List[str] = []