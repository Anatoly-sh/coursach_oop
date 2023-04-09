import os

from dotenv import load_dotenv
from engine_cl import HH, SJ
from connector import Connector

from utils.functions import *

load_dotenv()
search_str: str = os.getenv('search_str')  # поисковая фраза по умолчанию
set_experience = '0'  # флаг "опыт работы"
load_data_volume_default = 500  # общее количество запрашиваемых вакансий с платформы по API по умолчанию
per_page_default = 50  # количество запрашиваемых вакансий на одной странице по умолчанию


menu_options = {
    1: 'Флаг "без опыта работы"',
    2: 'Запросить/обновить данные с сайтов вакансий в локальных файлах',
    3: 'Посмотреть вакансии в указанном городе',
    4: 'Вывести 10 самых высокооплачиваемых вакансий',
    5: 'Запись обрабатываемых вакансий в файл json',
    6: 'Завершение программы',
}


def print_menu():
    print('\n                    Программа "Парсер вакансий"\n'
          'выполняет поиск вакансий посредством API на сайтах HeadHunter и SuperJob')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def load_data():
    """
    Запрашивает параметры и выполняет загрузку данных с сайтов HH и SJ с сохранением
    в HH_vacancies.json и в SJ_vacancies.json
    """
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

    # Формирование экз. класса HH, затем - SJ
    hh = HH(new_search_str, set_experience, load_data_volume, per_page)
    # Вызов метода загрузки данных с сайта, параметры: поисковая строка/опыт/объем данных/количество на странице ответа
    hh.request_and_write_data()

    sj = SJ(new_search_str, set_experience, load_data_volume, per_page)
    sj.request_and_write_data()


def show_town_list():
    """
    Корректирует названия городов (с заглавной буквы + составные названия)
    и выводит вакансии по указанному городу (если имеются)
    """
    print('Выбрана опция \'show_town_list\'')
    search_town = 'Москва'
    input_string = input('Введите название города (по умолчанию - Москва):')
    if len(input_string) > 2:
        search_town = input_string.title()
        if '-' in search_town:
            search_town = search_town.split('-')
            for item in search_town:
                item.title()
            search_town = '-'.join(search_town)
        search_town = search_town.title()
    # сумма списков экземпляров класса Vacancy из двух источников
    unsorted_vacancy_list = Connector.vacancy_selection_hh()[0] + Connector.vacancy_selection_sj()[0]
    print(f'Поиск по городу: {search_town}:')
    for item in unsorted_vacancy_list:
        if item.city == search_town:
            print(f'{item.city}: ', item)


def show_top_10():
    """
    Выводит 10 самых высокооплачиваемых вакансий
    """
    print('10 самых высокооплачиваемых вакансий:')
    unsorted_vacancy_list = Connector.vacancy_selection_hh()[0] + Connector.vacancy_selection_sj()[0]
    unsorted_vacancy_list.sort(key=lambda k: k.salary_from, reverse=True)
    sorted_by_salary_list = unsorted_vacancy_list                       # сортированный по зарплате
    for item in range(10):
        print(f'{item + 1} -- {sorted_by_salary_list[item]}')


def write_current_json_file():
    """
    Запись в файл формата json вакансий из источников HH и SJ с отобранными параметрами
    """
    unsorted_vacancy_list_dict = Connector.vacancy_selection_hh()[1] + Connector.vacancy_selection_sj()[1]
    jf = input('Введите имя файла: ')
    Connector.wr_json_file(jf, unsorted_vacancy_list_dict)


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
            write_current_json_file()
        elif option == 6:
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 6')
