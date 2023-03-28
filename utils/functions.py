import json
import re
from engine_cl import Vacancy

pattern = '<[^<]+?>'
unsorted_vacancy_list = []


def clean_text(param, param1):
    return re.sub(param, "", param1)


def sorted_list_vac(list_name):
    """
    с сортировкой не справился
    """
    list_name.sort(key=lambda k: k.salary_from, reverse=True)


def vacancy_selection_hh():
    """
    выполняет выборку данных из файла json HH и помещает в список вакансий
    """
    with open('./HH_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for page in data.values():
            for i in range(len(page['items'])):
                path_vacancy = page['items'][i]
                # формирование словаря для экземпляров класса по вакансиям HH
                hh_dict = {'source': 'HeadHunter',
                           'name_vac': path_vacancy['name'],                                    # профессия
                           'id': path_vacancy['id'],                                            # номер id
                           'city': path_vacancy['area']['name'],                                # город
                           'description': path_vacancy['snippet'].get('requirement', 0),
                           'responsibility': path_vacancy['snippet'].get('responsibility', 0)
                           }
                # если параметров нет в json:
                if path_vacancy.get('salary', 0) is None:
                    hh_dict['salary_from'] = 0
                    hh_dict['currency'] = 0
                else:
                    hh_dict['salary_from'] = path_vacancy['salary'].get('from', 0)              # зарплата
                    hh_dict['currency'] = path_vacancy['salary'].get('currency', 0)             # валюта
                name_inst_vacancy_hh = f"HH_{hh_dict['id']}"
                print(name_inst_vacancy_hh)
                name_inst_vacancy_hh = Vacancy(hh_dict)
                unsorted_vacancy_list.append(name_inst_vacancy_hh)


def vacancy_selection_sj():
    """
    выполняет выборку данных из файла json SJ и помещает в список вакансий
    """
    with open('./SJ_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        # для каждой страницы (ключ - страница вакансий)
        for page in data.values():
            # print(len(page['objects']))
            for i in range(len(page['objects'])):
                path_vacancy = page['objects'][i]

                # формирование словаря для экземпляров класса по вакансиям SJ
                sj_dict = {'source': 'SuperJob',
                           'name_vac': path_vacancy.get('profession', 0),       # профессия
                           'id': path_vacancy['id'],                            # номер id
                           'city': path_vacancy['town'].get('title', 0),        # город
                           'salary_from': path_vacancy['payment_from'],         # зарплата
                           'currency': path_vacancy['currency'],                # валюта
                           'description': path_vacancy['candidat'],
                           'responsibility': path_vacancy['client'].get('description', 0)
                           }
                name_inst_vacancy_sj = f"SJ_{sj_dict['id']}"
                print(name_inst_vacancy_sj)
                name_inst_vacancy_sj = Vacancy(sj_dict)
                unsorted_vacancy_list.append(name_inst_vacancy_sj)
