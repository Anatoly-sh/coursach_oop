class Connector:
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
        pass

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

# ______________________________________________________________________________________________
class Connector:
    """
    Класс проверяет состояния json файлов, готовит параметры для
    формирования экземпляров класса Vacancy из скачанных вакансий
    """
    # пустой список для отсортированных вакансий (потом перенести в main)
    UNSORTED_LIST = []
    hh_dict = {'source': 'HeadHunter',
               'name_vac': item['name'],                    # профессия
               'url': item['alternate_url'],                # url
               'city': item['area']['name'],                # город
               'salary_from': item['salary']['from'],       # зарплата
               'currency': item['salary']['currency'],      # RUR
               }
    if item['snippet']['requirement'] is not None:
        hh_dict['description'] =  clean_text(pattern, item['snippet']['requirement'])
    if item['snippet']['responsibility'] is not None:
        hh_dict['responsibility'] = clean_text(pattern, item['snippet']['responsibility'])

    sj_dict = {'source': 'SuperJob',
               'name_vac': item['profession'],          # профессия
               'url': item['client']['link'],           # url
               'city': item['client']['town']['title'], # город
               'salary_from': item['payment_from'],     # зарплата
               'currency': item['currency'],            # RUR
               }
    if item['candidat'] is not None:
        sj_dict['description'] = clean_text(pattern, item['candidat'])
    if item['client']['description'] is not None:
        sj_dict['responsibility'] = clean_text(pattern, item['client']['description'])

    def __init__(self):
        pass

    def HH_search(self):
        with open('./HH_vacancies.json', 'r') as file:



