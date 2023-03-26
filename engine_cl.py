import json
import os
from abc import ABC, abstractmethod
import requests
from requests import Response
from typing import List
from pprint import pprint

# from funcs_for_parsing_hh import *
# from funcs_for_parsing_sj import *
from dotenv import load_dotenv

load_dotenv()

api_key: str = os.getenv('SUPERJOB_API_KEY')


class Engine(ABC):
    """
    Абстрактный базовый класс для формирования классов HH и SJ,
    работающих с сервисами поиска работы
    """

    @abstractmethod
    def get_request(self, url: str, params: dict):
        """
        Абстрактный метод, отправляющий запрос на тот или иной сайт вакансий.
        url: url запроса
        params: параметры запроса
        """
        try:
            response = requests.get(url=url, params=params)
            if response.status_code != 200:
                raise LookupError(f'Статус код {response.status_code}')
            if not response:
                raise LookupError('Нет ответа')
            return response
        except (requests.exceptions.RequestException, LookupError) as error:
            print(f'Не могу получить данные, {error}')

    # @abstractmethod # прверить необходимость
    # def write_data(self, data):
    #     """
    #     Абстрактный метод, записывающий полученные в запросе данные
    #     в файл (имя???)
    #     :param data: неотформатированные данные, полученные от сервиса
    #     """
    #     pass


class HH(Engine):
    """
    Класс, описывающий сервис поиска работы на HeadHunter.
    (в случае другого источника формируется аналогичный класс)
    Args:
        search (str): поисковый запрос (название вакансии формируется в меню main, по умолчанию - Python)
        experience (str): параметр, отвечающий за поиск вакансий без требования опыта
        (название вакансии формируется в меню main)
    Attrs:
        url (str): url API HeadHunter
        params (dict): параметры API запроса
    """

    def __init__(self, search: str, experience: str):
        self.search = search
        self.url = 'https://api.hh.ru/vacancies/'
        self.params = {
            'text': f'NAME:{self.search}',
            'per_page': 100, # заменить на 100
            'page': 0,
            'area': '113'
        }

        if experience == '1':
            self.params['experience'] = 'noExperience'  # добавляем в словарь параметров

    def get_request(self, url: str, params: dict):
        return super().get_request(self.url, self.params)     # строка запроса из класса Engine

    def request_and_write_data(self):
        print('\nHH:__________________________________')
        with open('./HH_vacancies.json', 'w+') as file:
            # словарь с данными
            data_list = {}
            for i in range(5):  # заменить на 5 или 10
                self.params['page'] = i
                print(str(i), end=' ')
                data_of_page = self.get_request(self.url, self.params).json()
                # добавляем данные в словарь
                data_list[i + 1] = data_of_page
            json.dump(data_list, file, ensure_ascii=False)


class SJ(Engine):
    """
    Класс, описывающий сервис поиска работы на HeadHunter.
    (в случае другого источника формируется аналогичный класс)
    Args:
        search (str): поисковый запрос (название вакансии формируется в меню main, по умолчанию - Python)
        experience (str): параметр, отвечающий за поиск вакансий без требования опыта
    Attrs:
        url (str): url API SuperJob
        params (dict): параметры API запроса
    """
    header = {"X-Api-App-Id": api_key}

    def __init__(self, search: str, no_experience: str):
        self.search = search
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {
            'keywords': self.search,
            'id_country': '1',
            'count': 50,
            'page': 1}
        if no_experience == '1':
            self.params['without_experience'] = 1

    def get_request(self, url: str, headers: str, params: dict):
        try:
            response = requests.get(url=self.url, headers=self.header, params=self.params)
            if response.status_code != 200:
                raise LookupError(f'Статус код {response.status_code}')
            if not response:
                raise LookupError('Нет ответа')
            return response
        except (requests.exceptions.RequestException, LookupError) as error:
            print(f'Не могу получить данные, {error}')

    def request_and_write_data(self):
        print('\nSJ:__________________________________')
        with open('./SJ_vacancies.json', 'w+') as file:
            # словарь с данными
            data_list = {}
            for i in range(10):
                self.params['page'] = i
                print(str(i), end=' ')
                data_of_page = self.get_request(url=self.url, headers=self.header, params=self.params).json()
                # добавляем данные в словарь
                data_list[i + 1] = data_of_page
            json.dump(data_list, file, ensure_ascii=False)


class Vacancy:
    __slots__ = ('source', 'name_vac', 'url', 'city', 'salary_from', 'currency', 'description', 'responsibility')

    def __init__(self, data: dict):
        self.source = data['source']
        self.name_vac = data['name_vac']
        self.url = data['url']
        self.city = data['city']
        self.salary_from = data['salary_from']
        self.currency = data['currency']
        self.description = data['description']
        self.responsibility = data['responsibility']

    def __gt__(self, other):
        return self.salary_from > other.salary_from

    def __lt__(self, other):
        return self.salary_from < other.salary_from

    def __repr__(self):
        return f'Источник: {self.source}, ' \
               f'вакансия: {self.name_vac}, ' \
               f'город: {self.city}, ' \
               f'зарплата от: {self.salary_from}'




# проверка Vacancy
# data1 = {'source': 1, 'name_vac': 2, 'url': 3, 'city': 4, 'salary_from': 5, 'description': 6}
# data2 = {'source': 1, 'name_vac': 2, 'url': 3, 'city': 4, 'salary_from': 55, 'description': 6}
#
# v1 = Vacancy(data1)
# v2 = Vacancy(data2)
#
# print(v1.__slots__)
# print(v1.__repr__)
# print(v1.source)
# print(v1.salary_from < v2.salary_from)


# проверка записи в файл SJ
# sj = SJ('Python', '1')
# pprint(h.params)    # +
# pprint(h.get_request(h.url, h.params))    # +
# sj.write_data(sj.get_request(sj.url, sj.header, sj.params))    # +


# проверка записи в файл HH
# h = HH('Python', '1')
# pprint(h.params)    # +
# pprint(h.get_request(h.url, h.params))    # +
# h.write_data(h.get_request(h.url, h.params))    # +



