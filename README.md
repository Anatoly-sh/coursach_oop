Парсер для сайтов HeadHunter и SuperJob собирает текущие вакансии по запросу пользователя.

Структура репозитория:

main.py - файл для запуска программы
engine_cl - файл классов: 
    class Engine(ABC) - родительский 
    сlass HH(Engine) и class SJ(Engine) - для работы с сайтами
    class Vacancy - класс, описывающий вакансии
    class Connector - класс для взаимодействия с файлами
utils - директория функций: functions.py - функции для работы программы

requirements.txt - список необходимых пакетов для работы с программой
Перед началом работы программы необходимо:

установить виртуальное окружение
установить пакеты из файла requirements.txt
для работы с API SuperJob нужно получить токен - https://api.superjob.ru/#gettin и установить его в 
переменные окружения, определив переменной 'SUPERJOB_API_KEY'

Описание работы программы:

Программа запрашивает вакансию, по которой будет производиться запрос
Просит выбрать какие вакансии искать - с опытом или без
Количество запрашиваемых вакансий > 500+500
Выводит меню
Программа работает со списком вакансий в памяти. json файл формируется для файлового способа обработки. 
Он, как и методы в классе Connector (select/insert/delete/connect) в логике не используется и выполнены,
т.к. должны присутствовать по заданию. Но могут использоваться для развития программы.