from sqlmodel import SQLModel
from typing import List, Optional

class PersonUpdate(SQLModel):
    NameSurnamePatronymic: Optional[str] = None
    Mail: Optional[List[str]] = None
    Gender: Optional[str] = None
    Nationality: Optional[str] = None
    Age: Optional[int] = None