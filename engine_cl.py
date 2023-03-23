import os
from abc import ABC, abstractmethod
import requests
from requests import Response
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag
from pprint import pprint

from funcs_for_parsing_hh import *
from funcs_for_parsing_sj import *
# import Vacancy
from dotenv import load_dotenv

load_dotenv()

api_key: str = os.getenv('SUPERJOB_API_KEY')


class Engine(ABC):
    """
    Абстрактный базовый класс для формирования классов HH и SJ,
    работающих с сервисами поиска работы
    """

    @abstractmethod
    def get_request(self, url: str, params: dict) -> Response | list:
        """
        Абстрактный метод, отправляющий запрос на тот или иной сайт вакансий.
        :param url: url запроса
        :param params: параметры запроса
        :return: ответ от сервиса или пустой список в случае ошибки
        """
        try:
            response = requests.get(url=url, params=params)
            if response.status_code != 200:
                raise LookupError(f'Статус код {response.status_code}')
            if not response:
                return []
            if not response:
                raise LookupError('Ответ пустой')
            return response
        except (requests.exceptions.RequestException, LookupError) as error:
            print(f'Не могу получить данные, {error}')
            return []

    @abstractmethod
    def write_data(self, data):
        """
        Абстрактный метод, записывающий полученные в запросе данные
        в файл (имя???)
        :param data: неотформатированные данные, полученные от сервиса
        """
        pass


class HH(Engine):
    """
    Класс, описывающий сервис поиска работы на HeadHunter.
    (в случае другого источника формируется аналогичный класс)
    Args:
        search (str): поисковый запрос (название вакансии)
        no_experience (str): параметр, отвечающий за поиск вакансий, где не нужен опыт
    Attrs:
        url (str): url API HeadHunter
        params (dict): параметры API запроса
    """

    def __init__(self, search: str, no_experience: str) -> None:
        self.search = search
        self.url = 'https://api.hh.ru/vacancies/'
        self.params = {
            'text': f'NAME:{self.search}',
            'per_page': 10,
            'page': 0,
            'area': '113'
        }

        if no_experience == '1':
            self.params['experience'] = 'noExperience'  # добавляем в словарь параметров

    def get_request(self, url: str, params: dict) -> Response | list:
        return super().get_request(self.url, self.params)     # строка запроса из класса Engine

    def write_data(self, data):
        print('HH:__________________________________')
        with open('./HH_vacancies.txt', 'w+') as file:
            for i in range(2):
                self.params['page'] = i
                print(str(i), end=' ')
                response = self.get_request(url=self.url, params=self.params).json()
                pprint(response, stream=file)


class SJ(Engine):
    """
    Класс, описывающий сервис поиска работы SuperJob.
    (в случае другого источника формируется аналогичный класс)
    Args:
        search (str): поисковый запрос (название вакансии)
        no_experience (str): параметр, отвечающий за поиск вакансий, где не нужен опыт
    Attrs:
        url (str): url API HeadHunter
        params (dict): параметры API запроса
    """
    header = {"X-Api-App-Id": api_key}

    def __init__(self, search: str, no_experience: str) -> None:
        self.search = search
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {'keywords': self.search, 'id_country': '1', 'count': 100, 'page': 1}
        if no_experience == '1':
            self.params['without_experience'] = 1

    def get_request(self, url: str, headers: str, params: dict) -> Response | list:
        return requests.get(url=self.url, headers=self.header, params=self.params)

    def write_data(self, data):
        print('SJ:__________________________________')
        with open('./SJ_vacancies.txt', 'w+') as file:
            for i in range(2):
                self.params['page'] = i
                print(str(i), end=' ')
                response = self.get_request(url=self.url, headers=self.header, params=self.params).json()
                pprint(response, stream=file)


# проверка записи в файл SJ
sj = SJ('Python', '1')
# pprint(h.params)    # +
# pprint(h.get_request(h.url, h.params))    # +
sj.write_data(sj.get_request(sj.url, sj.header, sj.params))    # +


# проверка записи в файл HH
# h = HH('Python', '1')
# pprint(h.params)    # +
# pprint(h.get_request(h.url, h.params))    # +
# h.write_data(h.get_request(h.url, h.params))    # +



