import json
from pprint import pprint

# from jsonschema import validate

from engine_cl import Vacancy
from utils.functions import clean_text

pattern = '<[^<]+?>'            # pattern для очистки текста от тегов
# unsorted_vacancy_list = []
# unsorted_vacancy_list_dict = []


class Connector:
    def __init__(self, file_path: str):
        self.data_file = file_path

    @staticmethod
    def vacancy_selection_hh(unsorted_vacancy_list: list, unsorted_vacancy_list_dict: list):
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
                               'name_vac': path_vacancy['name'],  # профессия
                               'id': path_vacancy['id'],  # номер id
                               'city': path_vacancy['area']['name'],  # город
                               }
                    # если параметров нет в json или параметр None - избавляемся:
                    # 'description': clean_text(pattern, path_vacancy['snippet'].get('requirement', 0))
                    if path_vacancy['snippet'].get('requirement', 0) is not None:
                        hh_dict['description'] = \
                            clean_text(pattern, path_vacancy['snippet'].get('requirement', 0))
                    else:
                        hh_dict['description'] = " "

                    if path_vacancy['snippet'].get('responsibility', 0) is not None:
                        hh_dict['responsibility'] = \
                            clean_text(pattern, path_vacancy['snippet'].get('responsibility', 0))
                    else:
                        hh_dict['responsibility'] = " "

                    if path_vacancy.get('salary') is None:
                        hh_dict['salary_from'] = 0
                        hh_dict['currency'] = 0
                    elif path_vacancy['salary'].get('from') is None:
                        hh_dict['salary_from'] = 0
                        hh_dict['currency'] = 0
                    else:
                        hh_dict['salary_from'] = path_vacancy['salary'].get('from', 0)  # зарплата
                        hh_dict['currency'] = path_vacancy['salary'].get('currency', 0)  # валюта

                    unsorted_vacancy_list.append(Vacancy(hh_dict))          # анализируемый список (10 лучших + города)
                    unsorted_vacancy_list_dict.append(hh_dict)              # для формирования json-файла

    @staticmethod
    def vacancy_selection_sj(unsorted_vacancy_list: list, unsorted_vacancy_list_dict: list):
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
                               'name_vac': path_vacancy.get('profession', 0),   # профессия
                               'id': path_vacancy['id'],  # номер id
                               'city': path_vacancy['town'].get('title', 0),    # город
                               'salary_from': path_vacancy['payment_from'],     # зарплата
                               'currency': path_vacancy['currency'],            # валюта
                               'description': path_vacancy['candidat'],
                               'responsibility': path_vacancy['client'].get('description', 0)
                               }
                    # обрезка длинных строк
                    # if len(sj_dict['responsibility']) > 200:
                    #     var = sj_dict['responsibility']
                    #     sj_dict['responsibility'] = var[:200] + '..'

                    # name_inst_vacancy_sj = f"SJ_{sj_dict['id']}"
                    # # print(name_inst_vacancy_sj)
                    # name_inst_vacancy_sj = Vacancy(sj_dict)
                    unsorted_vacancy_list.append(Vacancy(sj_dict))
                    unsorted_vacancy_list_dict.append(sj_dict)          # для формирования json-файла

    @staticmethod
    # connect
    def wr_json_file(file, vacancy_list):
        with open(file, 'w+') as json_file:
            json.dump(vacancy_list, json_file, indent=2, ensure_ascii=False)

    def connect(self):
        """
               Создание файла с пустым списком или его перезапись
        """
        with open(self.data_file, 'w') as file:
            json.dump([], file)

    def insert(self, data: dict) -> None:
        """Добавление данных в файл"""
        with open(self.data_file, 'r', encoding='UTF-8') as file:
            data_json = json.load(file)
            data_json.append(data)
        with open(self.data_file, 'w', encoding='UTF-8') as file:
            json.dump(data_json, file, indent=2, ensure_ascii=False)

    def select(self, query: dict) -> list:
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение

        """
        result = []
        with open(self.data_file, 'r') as json_file:
            data = json.load(json_file)
        if not query:
            return data             # все данные
        for item in data:
            if all(item.get(key) == value for key, value in query.items()):
                result.append(item)
        return result

    def delete(self, query: dict) -> list | None:
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not query:
            return
        with open(self.data_file) as f:
            data = json.load(f)

        result = []
        for item in data:
            if not all(item.get(key) == value for key, value in query.items()):     # select наоборот
                result.append(item)

        with open(self.data_file, 'w') as file:
            json.dump(result, file, indent=2, ensure_ascii=False)



if __name__ == '__main__':
    df = Connector('tmp.json')
    # df.connect()
    data_for_file = {'id': 1, 'title': 'tet'}
    #
    df.insert(data_for_file)
    data_from_file = df.select(dict())
    data_from_file = df.select(data_for_file)
    print(data_from_file)
    assert data_from_file == [data_for_file]

    df.delete({'id': 1})
    data_from_file = df.select(dict())
    assert data_from_file == []
