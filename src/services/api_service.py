import requests
from abc import ABC, abstractmethod
import re
from typing import List, Union
from transliterate import translit

class APIHandler(ABC):
    #Метод для получение ответа для одного человека
    @abstractmethod
    def get_info(self, name: str) -> str:
        pass
    
    #Метод для получение ответа для нескольких людей
    @abstractmethod
    def get_batch_info(self, names: List[str]) -> List[str]:
        pass

class AgeHandler(APIHandler):
    #Обработка ФИО и перевод фамилии в англ. формат
    def _prepare_name(self, name: str) -> str:
        first_name = name.split()[0]
        if re.search('[а-яА-ЯёЁ]', first_name):
            return translit(first_name, 'ru', reversed=True)
        return first_name

    def get_info(self, name: str) -> str:
        prepared_name = self._prepare_name(name)
        response = requests.get(
            "https://api.agify.io",
            params={"name": prepared_name}
        )
        return str(response.json()["age"])

    def get_batch_info(self, names: List[str]) -> List[str]:
        prepared_names = [self._prepare_name(n) for n in names]
        params = [("name[]", name) for name in prepared_names]
        response = requests.get("https://api.agify.io", params=params)
        return [str(item["age"]) for item in response.json()]

class GenderHandler(APIHandler):
    def get_info(self, name: str) -> str:
        response = requests.get(
            "https://api.genderize.io",
            params={"name": name}
        )
        return response.json()["gender"]

    def get_batch_info(self, names: List[str]) -> List[str]:
        params = [("name[]", name) for name in names]
        response = requests.get("https://api.genderize.io", params=params)
        return [item["gender"] for item in response.json()]

class NationalityHandler(APIHandler):
    def get_info(self, name: str) -> str:
        response = requests.get(
            "https://api.nationalize.io",
            params={"name": name}
        )
        return response.json()["country"][0]["country_id"]

    def get_batch_info(self, names: List[str]) -> List[str]:
        params = [("name[]", name) for name in names]
        response = requests.get("https://api.nationalize.io", params=params)
        return [item["country"][0]["country_id"] for item in response.json()]

class HandlerFactory:
    @staticmethod
    def get_handler(character: str) -> APIHandler:
        return {
            "age": AgeHandler(),
            "gender": GenderHandler(),
            "nationality": NationalityHandler()
        }[character]

#Обработчик информации для определение нужного класса и метода
def get_info(name: Union[str, List[str]], character: str) -> Union[str, List[str]]:
    handler = HandlerFactory.get_handler(character)
    if isinstance(name, list):
        return handler.get_batch_info(name)
    return handler.get_info(name)