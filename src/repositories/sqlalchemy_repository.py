from typing import Generic, Type, TypeVar, Optional, List
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlmodel import SQLModel
from sqlalchemy.orm import selectinload

from ..models import PersonInfo, PersonMail
from .base_repository import AbstractRepository
from ..config.database import db_helper1
from ..config import settings

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

#Основной класс для выполнения CRUD-операций
class PeopleRepository(AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db_helper = db_helper1

    #Создание одной записи
    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self.db_helper.get_db_session() as session:
            person_data = data.model_dump(exclude={"Mail"})
            instance = self.model(**person_data)
            session.add(instance)
        
            await session.flush()
        
            if data.Mail:
                emails_to_add = [
                    PersonMail(Mail=email, PersonInfoId=instance.Id)
                    for email in data.Mail
                ]
                session.add_all(emails_to_add)
            
            await session.refresh(instance, attribute_names=["emails"])
            await session.commit()
        
            return instance
    
    #Создание нескольких записей
    async def bulk_create(self, data_list: List[CreateSchemaType]) -> List[ModelType]:
        async with self.db_helper.get_db_session() as session:
            try:
                people_instances = []
                all_emails = []
                for data in data_list:
                    #Исключая почту создает словари с данными о человеке
                    person_data = data.model_dump(exclude={"Mail"})
                    instance = self.model(**person_data)
                    people_instances.append(instance)
                    
                    #Создает таблицу почт с временными Id
                    if data.Mail:
                        all_emails.extend([
                            {"Mail": email, "temp_id": id(instance)}
                            for email in data.Mail
                        ])
                #Предзагружает данные в БД, Связывает данные, закрывает сессию
                session.add_all(people_instances)
                await session.flush()
                
                id_mapping = {id(inst): inst.Id for inst in people_instances}
                
                emails_to_add = [
                    PersonMail(
                        Mail=email["Mail"], 
                        PersonInfoId=id_mapping[email["temp_id"]]
                    )
                    for email in all_emails
                ]
                
                if emails_to_add:
                    session.add_all(emails_to_add)
                
                await session.commit()
                return people_instances
                
            except Exception as e:
                await session.rollback()
                raise e
            
    #Обновление записи
    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        async with self.db_helper.get_db_session() as session:
            update_data = data.model_dump(
                exclude_unset=True,
                exclude={"Mail"}
            )
            
            sql_request = (
                update(self.model)
                .values(**update_data)
                .filter_by(**filters)
                .returning(self.model)
            )
            result = await session.execute(sql_request)
            instance = result.scalar_one()
            
            if data.Mail is not None:
                await session.execute(
                    delete(PersonMail)
                    .where(PersonMail.PersonInfoId == instance.Id)
                )
                for email in data.Mail:
                    session.add(
                        PersonMail(Mail=email, PersonInfoId=instance.Id)
                    )
            
            await session.commit()
            await session.refresh(instance, attribute_names=["emails"])
            return instance

    #Удаление записи
    async def delete(self, **filters) -> None:
        async with self.db_helper.get_db_session() as session:
            instance = await session.execute(
                select(self.model).filter_by(**filters)
            )
            instance = instance.scalar_one_or_none()

            if instance:
                await session.execute(
                    delete(PersonMail)
                    .where(PersonMail.PersonInfoId == instance.Id)
                )
                await session.delete(instance)
                await session.commit()

    #Получение записи по фамилии
    async def get_by_surname(self, surname: str) -> Optional[ModelType]:
        async with self.db_helper.get_db_session() as session:
            query = select(self.model).filter(
                self.model.NameSurnamePatronymic.startswith(f"{surname} ")
            )
            
            if self.model == PersonInfo:
                query = query.options(selectinload(PersonInfo.emails))
                
            result = await session.execute(query)
            return result.scalars().first()
        
    #Получить все записи
    async def get_all(
        self,
        order: str = "Id",
        limit: int = settings.LIMIT, #Ограничение
        offset: int = 0
    ) -> List[ModelType]:
        async with self.db_helper.get_db_session() as session:
            sql_request = select(self.model).order_by(order).limit(limit).offset(offset)
            if self.model == PersonInfo:
                sql_request = sql_request.options(selectinload(PersonInfo.emails))
            result = await session.execute(sql_request)
            return result.scalars().all()