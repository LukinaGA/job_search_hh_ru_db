from abc import ABC, abstractmethod

import requests


class Parser(ABC):

    @abstractmethod
    def load_vacancies(self) -> list[dict]:
        pass


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        """Инициализатор класса HeadHunterAPI"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: list[dict] = []

    @property
    def url(self) -> str:
        """Возвращает cвойство url"""
        return self.__url

    def __api_connect(self) -> requests.Response:
        """Подключение к API hh.ru"""
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            return response

        print("Ошибка получения данных")

    def load_vacancies(self) -> list:
        """Получение вакансий с hh.ru"""
        employers = ["Т-Банк", "СБЕР", "Комос Групп", "Skyeng", "Directum", "Ozon Банк", "Алабуга", "АО ИРЗ",
                     "Тэйсти Кофе", "Калашников"]
        for employer in employers:
            self.__params["text"] = employer
            while self.__params.get("page") != 1:
                response = self.__api_connect()
                if response:
                    vacancies = response.json()["items"]
                    self.__vacancies.extend(vacancies)
                    self.__params["page"] += 1
                else:
                    break

        return self.__vacancies
