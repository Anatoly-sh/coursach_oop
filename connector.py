import json
# from jsonschema import validate

from engine_cl import Vacancy


class Connector:
    @staticmethod
    def vacancy_selection_hh(unsorted_vacancy_list: list):
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
                               'description': path_vacancy['snippet'].get('requirement', 0),
                               'responsibility': path_vacancy['snippet'].get('responsibility', 0)
                               }
                    # если параметров нет в json или параметр - None:
                    if path_vacancy.get('salary') is None:
                        hh_dict['salary_from'] = 0
                        hh_dict['currency'] = 0
                    elif path_vacancy['salary'].get('from') is None:
                        hh_dict['salary_from'] = 0
                        hh_dict['currency'] = 0
                    else:
                        hh_dict['salary_from'] = path_vacancy['salary'].get('from', 0)  # зарплата
                        hh_dict['currency'] = path_vacancy['salary'].get('currency', 0)  # валюта
                    # name_inst_vacancy_hh = f"HH_{hh_dict['id']}"
                    # # print(name_inst_vacancy_hh)
                    # name_inst_vacancy_hh = Vacancy(hh_dict)
                    unsorted_vacancy_list.append(Vacancy(hh_dict))

    @staticmethod
    def vacancy_selection_sj(unsorted_vacancy_list: list):
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
                               'name_vac': path_vacancy.get('profession', 0),  # профессия
                               'id': path_vacancy['id'],  # номер id
                               'city': path_vacancy['town'].get('title', 0),  # город
                               'salary_from': path_vacancy['payment_from'],  # зарплата
                               'currency': path_vacancy['currency'],  # валюта
                               'description': path_vacancy['candidat'],
                               'responsibility': path_vacancy['client'].get('description', 0)
                               }
                    # name_inst_vacancy_sj = f"SJ_{sj_dict['id']}"
                    # # print(name_inst_vacancy_sj)
                    # name_inst_vacancy_sj = Vacancy(sj_dict)
                    unsorted_vacancy_list.append(Vacancy(sj_dict))



    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None
    @property
    def data_file(self):
        pass

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """


    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        pass

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        pass

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        pass


if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'id':1})
    data_from_file = df.select(dict())
    assert data_from_file == []
