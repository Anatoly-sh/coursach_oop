import os
from pprint import pprint

from dotenv import load_dotenv
from engine_cl import HH, SJ, Engine
from connector import Connector

from utils.functions import *

# from engine_cl import load_data_volume
load_dotenv()
search_str: str = os.getenv('search_str')  # поисковая фраза по умолчанию
set_experience = '0'  # флаг "опыт работы"
load_data_volume_default = 500  # общее количество запрашиваемых вакансий с платформы по API по умолчанию
per_page_default = 50  # количество запрашиваемых вакансий на одной странице по умолчанию
unsorted_vacancy_list = []
unsorted_vacancy_list_dict = []

menu_options = {
    1: 'Флаг "без опыта работы"',
    2: 'Запросить/обновить данные с сайтов вакансий в локальных файлах',
    3: 'Посмотреть вакансии в указанном городе',
    4: 'Вывести 10 самых высокооплачиваемых вакансий',
    5: 'Операции с файлом json',
    6: 'Завершение программы',
}


def print_menu():
    print('\n                    Программа "Парсер вакансий"\n'
          'выполняет поиск вакансий посредством API на сайтах HeadHunter и SuperJob')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def load_data():
    print(f'По умолчанию поиск вакансий выполняется по ключевой фразе "{search_str}"')
    input_string = input('Введите фразу для поиска (с разделителями ; , / :)или "Enter":')
    if len(input_string) > 2 and input_string.isalpha():
        new_search_str = re.split(";|,| |/|:", input_string)
    else:
        new_search_str = search_str
    inp = input('Введите требуемое количество вакансий с каждой платформы (сайта) - по умолчанию 500:')
    if inp != "":
        load_data_volume = int(inp)
    else:
        load_data_volume = load_data_volume_default
    inp = input('Введите требуемое количество вакансий на странице - по умолчанию 50:')
    if inp != "":
        per_page = int(inp)
    else:
        per_page = per_page_default
    print(load_data_volume)
    print(per_page)

    # формирование экз. класса HH, затем - SJ
    hh = HH(new_search_str, set_experience, load_data_volume, per_page)
    # вызов метода загрузки данных с сайта, параметры: поисковая строка/опыт/объем данных/количество на странице ответа
    hh.request_and_write_data()

    sj = SJ(new_search_str, set_experience, load_data_volume, per_page)
    sj.request_and_write_data()


def show_town_list():
    print('Выбрана опция \'show_town_list\'')
    search_town = 'Москва'
    input_string = input('Введите название города (по умолчанию - Москва):')
    if len(input_string) > 2 and input_string.isalpha():
        search_town = input_string
    # if len(unsorted_vacancy_list) == 0:
    unsorted_vacancy_list.clear()
    unsorted_vacancy_list_dict.clear()
    conn = Connector()
    conn.vacancy_selection_hh(unsorted_vacancy_list, unsorted_vacancy_list_dict)
    conn.vacancy_selection_sj(unsorted_vacancy_list, unsorted_vacancy_list_dict)
    print(len(unsorted_vacancy_list))
    print(len(unsorted_vacancy_list))
    print(f'Поиск по городу: {search_town}:')
    for item in unsorted_vacancy_list:
        if item.city == search_town:
            print(f'{item.city}: ', item)


def show_top_10():
    print('Выбрана опция \'show_top_10\'')
    if len(unsorted_vacancy_list) == 0:
        conn = Connector()
        conn.vacancy_selection_hh(unsorted_vacancy_list)
        conn.vacancy_selection_sj(unsorted_vacancy_list)

    # vacancy_selection_hh(unsorted_vacancy_list)
    # vacancy_selection_sj(unsorted_vacancy_list)

    unsorted_vacancy_list.sort(key=lambda k: k.salary_from, reverse=True)
    # print(unsorted_vacancy_list[:10])   # REPR
    for item in range(10):
        print(unsorted_vacancy_list[item])


def file_i_o():
    print('\nВозможны следующие операции файлами:\n'
          '1 -- Сохранение текущего списка вакансий в файл json\n'
          '2 -- Добавление вакансии в файл json\n'
          '3 -- Удаление вакансий без указания зарплаты из файла json \n'
          '4 -- Сохранение текущего списка вакансий в файл csv')
    while True:
        input_cmd = input('Введите команду (1 - 4): ')
        try:
            input_cmd = int(input_cmd)
        except ValueError:
            print('Правильный номер, пожалуйста')
            continue
        if 1 <= input_cmd <= 4:
            break
        else:
            print('От 1 до 4, пожалуйста')

    conn = Connector()  # мб Connector.wr_json_file(jf)??????????????????????
    if input_cmd == 1:
        # print(len(unsorted_vacancy_list_dict))
        # for item in range(len(unsorted_vacancy_list_dict)):
        #     pprint(unsorted_vacancy_list_dict[item])
        jf = input('Введите имя файла: ')
        conn.wr_json_file(jf, unsorted_vacancy_list_dict)

    if input_cmd == 2:
        tst_vacancy = {'id': 1, 'title': 'tet'}
        conn.insert(tst_vacancy)

    if input_cmd == 3:
        conn.select(dict())

    if input_cmd == 4:
        conn.delete({'id': 1})


if __name__ == '__main__':
    while True:
        print_menu()
        option = ''
        try:
            option = int(input('Сделайте выбор: '))
        except:
            print('Неверный ввод. Пожалуйста введите цифру...')
        # Проверка выбора и действие
        if option == 1:
            if set_experience == '0':
                set_experience = '1'
                print(f'Флаг "без опыта работы" установлен')
            else:
                set_experience = '0'
                print(f'Флаг "без опыта работы" сброшен')
        elif option == 2:
            load_data()
        elif option == 3:
            show_town_list()
        elif option == 4:
            show_top_10()
        elif option == 5:
            file_i_o()
        elif option == 6:
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 6')
