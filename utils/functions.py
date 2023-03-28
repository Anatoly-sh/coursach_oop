import json
import re
from pprint import pprint
from engine_cl import Vacancy


pattern = '<[^<]+?>'
unsorted_vacancy_list = []


# удаление pattern
def clean_text(param, param1):
    return re.sub(param, "", param1)


def sort_list_vacancy(unsort_d: list):
    """
    с сортировкой не справился
    """
    # sorted_vacancy_list = sorted(unsorted_vacancy_list, key=lambda k: k.salary_from, reverse=True)
    return unsorted_vacancy_list


def vacancy_selection_hh():
    """
    выполняет выборку данных из файла json HH и помещает в список вакансий
    """
    with open('../HH_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for page in data.values():
            # print(page)
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
                if path_vacancy.get('salary') is None:
                    hh_dict['salary_from'] = 0
                    hh_dict['currency'] = 0
                else:
                    hh_dict['salary_from'] = path_vacancy['salary'].get('from', 0)              # зарплата
                    hh_dict['currency'] = path_vacancy['salary'].get('currency', 0)             # валюта

                name_inst_vacancy_hh = f"HH_{hh_dict['id']}"
                print(name_inst_vacancy_hh)
                # формирование экземпляров класса Vacancy и добавление в список
                name_inst_vacancy_hh = Vacancy(hh_dict)
                unsorted_vacancy_list.append(name_inst_vacancy_hh)


def vacancy_selection_sj():
    """
    выполняет выборку данных из файла json SJ и помещает в список вакансий
    """
    with open('../SJ_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        # для каждой страницы (ключ - страница вакансий)
        for page in data.values():
            # print(len(page['objects']))
            for i in range(len(page['objects'])):
                path_vacancy = page['objects'][i]
                # pprint(page['objects'][i]['client']['link'])
                # pprint(page['objects'][i]['profession'])

                # формирование словаря для экземпляров класса по вакансиям SJ
                sj_dict = {'source': 'SuperJob',
                           'name_vac': path_vacancy.get('profession', 0),       # профессия
                           'id': path_vacancy['id'],                            # номер id
                           'city': path_vacancy['town'].get('title', 0),        # город
                           'salary_from': path_vacancy.get('payment_from', 0),  # зарплата
                           'currency': path_vacancy['currency'],                # валюта
                           'description': path_vacancy['candidat'],
                           'responsibility': path_vacancy['client'].get('description', 0)
                           }

                name_inst_vacancy_sj = f"SJ_{sj_dict['id']}"
                print(name_inst_vacancy_sj)
                # формирование экземпляров класса Vacancy и добавление в список
                name_inst_vacancy_sj = Vacancy(sj_dict)
                unsorted_vacancy_list.append(name_inst_vacancy_sj)


if __name__ == '__main__':
    vacancy_selection_hh()
    vacancy_selection_sj()
    # print(len(UNSORTED_VACANCY_LIST))
    # for item in UNSORTED_VACANCY_LIST:
    #     print(item)
    # sorted_vacancies = sorted(UNSORTED_VACANCY_LIST, key=lambda x: x.salary_from, reverse=True)
    # UNSORTED_VACANCY_LIST.sort()
    # SORTED_VACANCY_LIST = sorted(UNSORTED_VACANCY_LIST, key=lambda k: k.salary_from, reverse=True)
    # print(SORTED_VACANCY_LIST[:10])
    print(len(unsorted_vacancy_list))
    # for item in UNSORTED_VACANCY_LIST:
    #     print(item.__str__)
    pprint(unsorted_vacancy_list[0:10])
