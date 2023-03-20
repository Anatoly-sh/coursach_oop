from datetime import date


def get_formatted_name_hh(unformatted_data: dict) -> str:
    """
    Возвращает название вакансии из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['name']


def get_formatted_url_hh(unformatted_data: dict) -> str:
    """
    Возвращает ссылку на вакансию из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['alternate_url']


def get_formatted_published_date_hh(unformatted_data: dict) -> date:
    """
    Возвращает дату (объект date) публикации вакансии из неотформатированных данных,
    полученных через API HeadHunter
    """
    date_str = unformatted_data['published_at']
    date_obj = date_str.split('T')[0]
    return date.fromisoformat(date_obj)


def get_formatted_description_hh(unformatted_data: dict) -> str:
    """
    Возвращает описание вакансии из неотформатированных данных,
    полученных через API HeadHunter
    """
    str_description = ''
    if unformatted_data['snippet']['requirement'] is not None:
        str_description += unformatted_data['snippet']['requirement']
    if unformatted_data['snippet']['responsibility'] is not None:
        str_description += '\n' + unformatted_data['snippet']['responsibility']
    return str_description.replace('<highlighttext>', '').replace('</highlighttext>', '')


def get_formatted_salary_hh(unformatted_data: dict) -> int:
    """
    Возвращает заработную плату из неотформатированных данных,
    полученных через API HeadHunter
    """
    salary_data = unformatted_data['salary']
    if salary_data is None or salary_data['from'] is None:
        return 0
    return salary_data['from']


def get_formatted_city_hh(unformatted_data: dict) -> str:
    """
    Возвращает город из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['area']['name']


def get_formatted_employer_hh(unformatted_data: dict) -> str:
    """
    Возвращает название компании из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['employer']['name']
