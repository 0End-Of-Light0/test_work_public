from typing import List
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel

from . import get_info
from . import EmailService
from ..models import PersonResponse, PersonCreate, PersonUpdate
from ..repositories import PeopleRepository


class PersonService:
    def __init__(self, repository: PeopleRepository):
        self.repository = repository
        self.model = repository.model

    #Преобразуем SQL модель для возврата данных в API
    @staticmethod
    def _to_response(person: SQLModel) -> PersonResponse:
        return PersonResponse(
            Id=person.Id,
            NameSurnamePatronymic=person.NameSurnamePatronymic,
            Gender=person.Gender,
            Nationality=person.Nationality,
            Age=person.Age,
            emails=[mail.Mail for mail in person.emails]
        )

    #Получаем человека по фамилии
    async def get_person(self, surname: str) -> PersonResponse:
        person = await self.repository.get_by_surname(surname)
        if not person:
            raise ValueError("Person not found")
        return self._to_response(person)

    #Получить всех людей
    async def get_all_people(self) -> List[PersonResponse]:
        people = await self.repository.get_all()
        return [self._to_response(person) for person in people]

    #Создать человека (Недостающие данные автоматически подтягиваются из API)
    async def create_person(self, person_data: PersonCreate) -> PersonResponse:
        try:
            # Проверка уникальности имени
            if await self.repository.get_by_surname(
                person_data.NameSurnamePatronymic
            ):
                raise ValueError("Person with this name already exists")
    
            # Валидация email
            if person_data.Mail:
                for email in person_data.Mail:
                    EmailService.validate_email_format(email)
    
            data = person_data.model_dump()
            
            # Автоматическое заполнение недостающих данных
            for field in ['Gender', 'Nationality', 'Age']:
                current_value = data.get(field)
                
                needs_replacement = (
                    current_value is None or
                    (isinstance(current_value, str) and not current_value.strip()) or
                    (isinstance(current_value, int) and current_value == 0) or
                    (isinstance(current_value, str) and current_value == "string")
                )
                
                if needs_replacement:
                    data[field] = get_info(
                        data['NameSurnamePatronymic'],
                        field.lower()
                    )
    
            validated_data = PersonCreate(**data)
            
            db_person = await self.repository.create(validated_data)
            return self._to_response(db_person)
    
        except IntegrityError as e:
            raise ValueError("Database integrity error") from e

    async def update_person(
        self,
        person_id: int,
        update_data: PersonUpdate
    ) -> PersonResponse:
        try:
            # Преобразование данных при необходимости
            if isinstance(update_data, dict):
                update_data = PersonUpdate(**update_data)

            # Остальная логика
            updated_person = await self.repository.update(
                update_data,  # Передаем модель, а не словарь
                Id=person_id
            )
            return self._to_response(updated_person)

        except IntegrityError as e:
            raise ValueError("Database integrity error") from e

    async def delete_person(self, person_id: int) -> None:
        """Удаление человека"""
        await self.repository.delete(Id=person_id)