import os
from pprint import pprint

from dotenv import load_dotenv
from engine_cl import HH, SJ
from utils.functions import *

load_dotenv()
search_str: str = os.getenv('search_str')
set_experience = 0

menu_options = {
    1: 'Установить флаг "без опыта работы"',
    2: 'Запросить/обновить данные с сайтов вакансий в локальных файлах',
    3: 'Посмотреть вакансии в указанном городе',
    4: 'Вывести 10 самых высокооплачиваемых вакансий',
    5: 'Завершение программы',
}


def print_menu():
    print('\n                    Программа "Парсер вакансий"\n'
          'выполняет поиск вакансий посредством API на сайтах HeadHunter и SuperJob')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def load_data():
    print('Выбрана опция \'load_data\'')
    print(f'По умолчанию поиск вакансий выполняется по ключевой фразе "{search_str}"')
    input_string = input('Введите фразу для поиска или "Enter":')
    if len(input_string) > 2 and input_string.isalpha():
        new_search_str = input_string
    else:
        new_search_str = search_str
    hh = HH(new_search_str, set_experience)
    hh.request_and_write_data()
    sj = SJ(new_search_str, set_experience)
    sj.request_and_write_data()
    vacancy_selection_hh()
    vacancy_selection_sj()


def show_town_list():
    print('Выбрана опция \'show_town_list\'')
    input_string = input('Введите название города (по умолчанию - Москва:')
    search_town = 'Москва'
    if len(input_string) > 2 and input_string.isalpha():
        search_town = input_string

    for item in unsorted_vacancy_list:
        if item.city == search_town:
            print(item)


def show_top_10():
    print('Выбрана опция \'show_top_10\'')
    pprint(unsorted_vacancy_list[0:10])


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
            if set_experience == 0:
                set_experience = 1
                print(f'Флаг "без опыта работы" установлен')
            else:
                set_experience = 0
                print(f'Флаг "без опыта работы" сброшен')
        elif option == 2:
            load_data()
        elif option == 3:
            show_town_list()
        elif option == 4:
            show_top_10()
        elif option == 5:
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 4')
