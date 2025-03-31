from fastapi import APIRouter, HTTPException, status

from .services import PersonService
from .models import PersonInfo, PersonResponse, PersonCreate, PersonUpdate
from .repositories import PeopleRepository


router = APIRouter(prefix="")


#Получение данных о человеке по фамилии
@router.get("/person/{name}", response_model=PersonResponse, tags=["person"])
async def get_person(
    name: str
):
    repo = PeopleRepository(PersonInfo)
    service = PersonService(repo)
    try:
        return await service.get_person(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#Получение всех людей в БД
@router.get("/people", response_model=list[PersonResponse], tags=["people"])
async def get_people():
    repo = PeopleRepository(PersonInfo)
    service = PersonService(repo)
    return await service.get_all_people()

#Создание новой записи в БД
@router.post("/person", response_model=PersonResponse, status_code=status.HTTP_201_CREATED, tags=["createperson"])
async def create_person(
    person: PersonCreate
):
    repo = PeopleRepository(PersonInfo)
    service = PersonService(repo)
    try:
        return await service.create_person(person)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Обновление данных человека
@router.patch("/person/{person_id}", response_model=PersonResponse, tags=["updateperson"])
async def update_person(
    person_id: int,
    person_data: PersonUpdate
):
    repo = PeopleRepository(PersonInfo)
    service = PersonService(repo)
    try:
        return await service.update_person(person_id, person_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Убрать при необходимости? Удаление человека из БД
@router.delete("/person/{person_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["deleteperson"])
async def delete_person(
    person_id: int
):
    repo = PeopleRepository(PersonInfo)
    service = PersonService(repo)
    try:
        await service.delete_person(person_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))