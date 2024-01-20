import json
import asyncio

from .data_mining_methods import (get_institutes_data,
                                  get_institutes_ids,
                                  get_groups_data)


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


if __name__ == '__main__':
    asyncio.run(update_json_data())
