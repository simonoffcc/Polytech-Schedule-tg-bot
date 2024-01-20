import json
import asyncio


from .parsing_methods import (_parse_institute_selection_page,
                              _parse_group_selection_page,
                              _parse_current_week_schedule)


async def get_institutes_data() -> list[dict]:
    data = await _parse_institute_selection_page()
    institutes_data = data['faculties']['data']
    if not isinstance(institutes_data, list):
        raise TypeError("Ошибка хранения информации об институтах в формате 'list[dict, ...]'!")
    return institutes_data


async def get_groups_data(institute_id: int) -> list[dict]:
    data = await _parse_group_selection_page(institute_id)
    groups_data = data['groups']['data'][str(institute_id)]
    if not isinstance(groups_data, list):
        raise TypeError("Ошибка хранения информации о группах в формате 'list[dict,...]'!")
    return groups_data


async def get_institutes_ids() -> list[int]:
    faculties = await get_institutes_data()
    institutes_ids = list(filter(None, (faculty.get('id') for faculty in faculties)))
    return institutes_ids


async def get_institutes_abbrs() -> list[str]:
    faculties = await get_institutes_data()
    institutes_abbrs = list(filter(None, (faculty.get('abbr') for faculty in faculties)))
    return institutes_abbrs


async def get_value_by_another_key(key_to_search: str,
                                   value_to_search: str | int,
                                   key_to_return_value: str) -> int | str | None:
    """
    Универсальный метод, который позволяет получить информацию из списка словарей по заданному ключу,
    в котором содержится переданное значение, относящееся к другому ключу.

    :param key_to_search: Ключ, по которому искать
    :param value_to_search: Значение, по которому найти словарь в списке
    :param key_to_return_value: Ключ, по которому вернуть значение из найденного словаря
    """
    faculties = await get_institutes_data()
    for faculty in faculties:
        if faculty.get(key_to_search) == value_to_search:
            return faculty.get(key_to_return_value)
    return


async def get_institutes_names() -> list[str]:
    faculties = await get_institutes_data()
    institutes_names = list(filter(None, (faculty.get('name') for faculty in faculties)))
    return institutes_names


async def convert_data_from_dict_to_str(data: dict) -> str:
    """Функция, которая преобразует данные из словаря в строку"""
    return '\n'.join(f"{key}: {value}" for key, value in data.items())


async def write_institutes_data() -> None:
    data = await get_institutes_data()
    with open(f'data/institutes_data.json', 'w') as file:
        json.dump(data, file, indent=4)


async def write_groups_data() -> None:
    faculties_ids = await get_institutes_ids()
    for faculty_id in faculties_ids:
        data = await get_groups_data(faculty_id)
        with open(f'data/faculty_{faculty_id}_data.json', 'w') as file:
            json.dump(data, file, indent=4)


async def update_json_data() -> None:
    await write_institutes_data()
    await write_groups_data()


institutes_acronyms: list[str] = asyncio.run(get_institutes_abbrs())


if __name__ == '__main__':
    asyncio.run(update_json_data())
