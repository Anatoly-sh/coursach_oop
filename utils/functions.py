import json
import re
from pprint import pprint

from engine_cl import Vacancy


pattern = '<[^<]+?>'
UNSORTED_VACANCY_LIST = []
def clean_text(param, param1):
    return re.sub(param, "", param1)


def sort_list_vacancy(unsort_d: list, sort_d: list):



def vacancy_selection_hh():
    with open('../HH_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for page in data.values():
            # print(page)
            for i in range(len(page['items'])):
                path_vacancy = page['items'][i]
                # print(i)
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
                # print(hh_dict['id'])
                name_inst_vacancy_hh = f"HH_{hh_dict['id']}"
                print(name_inst_vacancy_hh)
                name_inst_vacancy = Vacancy(hh_dict)
                UNSORTED_VACANCY_LIST.append(name_inst_vacancy_hh)


def vacancy_selection_sj():
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
                           'salary_from': path_vacancy['payment_from'],         # зарплата
                           'currency': path_vacancy['currency'],                # валюта
                           'description': path_vacancy['candidat'],
                           'responsibility': path_vacancy['client'].get('description', 0)
                           }
                name_inst_vacancy_sj = f"SJ_{sj_dict['id']}"
                print(name_inst_vacancy_sj)
                name_inst_vacancy = Vacancy(sj_dict)
                UNSORTED_VACANCY_LIST.append(name_inst_vacancy_sj)


                # print(sj_dict['responsibility'])
        #     if item['candidat'] is not None:
        #         sj_dict['description'] = clean_text(pattern, item['candidat'])
        #     if item['client']['description'] is not None:
        #         sj_dict['responsibility'] = clean_text(pattern, item['client']['description'])
        #
            # print('Super Job---------------------------')
            # print(item['profession'])
            # print(item['client']['link'])
            # print(item['client']['town']['title'])
            # print(item['payment_from'])
            # print(item['currency'])
            # if item['candidat'] is not None:
            #     print(clean_text(pattern, item['candidat']))
            # if item['client']['description'] is not None:
            #     print(clean_text(pattern, item['client']['description']))

if __name__ == '__main__':
    vacancy_selection_hh()
    vacancy_selection_sj()
    print(len(UNSORTED_VACANCY_LIST))
    # for item in UNSORTED_VACANCY_LIST:
    #     print(item.__str__)










"""
    data = 'qq;onefv;ojefovhreo;vce;ocj;eoc;oeic;eoaij;oeijc;oeij;oierj;foiejr;oije;ocije;oije;oij;eoij;eroij;oerija;eo'
    info = (data[:15] + '..') \
        if len(data) > 75 \
        else data
    print(info)"""