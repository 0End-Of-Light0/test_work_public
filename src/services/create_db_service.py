from sqlmodel import SQLModel
import random
from typing import List

from . import get_info
from ..models import PersonCreate, PersonInfo
from ..repositories import PeopleRepository
from ..config.database import db_helper1
from ..config import settings

async def initialize_database():
    #Создает отсутвующие таблицы в БД
    async with db_helper1.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with db_helper1.get_db_session() as session:
        people_repo = PeopleRepository(PersonInfo)
        
        existing_people = await people_repo.get_all()
        existing_names = {p.NameSurnamePatronymic for p in existing_people}
        
        # Определяет существуют ли в БД тестовые данные
        new_names = [
            name for name in settings.DEFAULT_PEOPLE_TEST_API
            if name not in existing_names
        ]
        
        if not new_names:
            print("All test data already exists")
            return

            #Взаимодействие с API
        try:
            genders = get_info(new_names, 'gender')
            nationalities = get_info(new_names, 'nationality')
            ages = get_info(new_names, 'age')
        except Exception as e:
            print(f"API Error: {str(e)}")
            return
    
        people_to_create: List[PersonCreate] = []
        for idx, full_name in enumerate(new_names):
            people_to_create.append(
                PersonCreate(
                    NameSurnamePatronymic=full_name,
                    Gender=genders[idx] or "",
                    Nationality=nationalities[idx] or "",
                    Age=ages[idx] or 0,
                    Mail=random.choice(settings.DEFAULT_MAIL_TEST)
                )
            )

        try:
            created_count = await people_repo.bulk_create(people_to_create)
            print(f"Successfully created {created_count} new people")
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise