import os
import re
from dotenv import load_dotenv

load_dotenv()
search_str: str = os.getenv('search_str')

menu_options = {
    1: 'Запросить/обновить данные с сайтов вакансий',
    2: 'Посмотреть вакансии в указанном городе',
    3: 'Вывести 10 самых высокооплачиваемых вакансий',
    4: 'Завершение программы',
}


def print_menu():
    print('                    Программа "Парсер вакансий"\n'
          'выполняет поиск вакансий посредством API на сайтах HeadHunter и SuperJob')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def load_data():
    print('Выбрана опция \'load_data\'')
    print(f'По умолчанию поиск вакансий выполняется по ключевой фразе {search_str}')
    input_string = input('Введите фразу для поиска:')
    if len(input_string) > 2 and input_string.isalpha():
        new_search_str = input_string
    else:
        new_search_str = search_str


def show_town_list():
    print('Выбрана опция \'show_town_list\'')
    input_string = input('Введите название города (по умолчанию - Москва:')
    if len(input_string) > 2 and input_string.isalpha():
        search_town = input_string
    else:
        search_town = 'Москва'



def show_top_10():
    print('Выбрана опция \'show_top_10\'')


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
            load_data()
        elif option == 2:
            show_town_list()
        elif option == 3:
            show_top_10()
        elif option == 4:
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 4')
