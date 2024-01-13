"""
class WrongInstituteAcronym(Exception):
    def __init__(self, acronym, message='Института с таким акронимом не найдено'):
        self.acronym = acronym
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Передано: {self.acronym} -> {self.message}'


class WrongGroupNumber(Exception):
    def __init__(self, group_number, message='Группы с таким номером не найдено'):
        self.group_number = group_number
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Передано: {self.group_number} -> {self.message}'


class UserBusiness:
    def __init__(self, telegram_id: int, faculty_acronym: str = "ИКНК", group_number: str = "5130904/20002"):
        self.telegram_id: int = telegram_id
        self.faculty: int = UserBusiness.is_valid_faculty(faculty_acronym)
        self.group_number: str = UserBusiness.is_valid_group(group_number)

    @staticmethod
    def is_valid_faculty(faculty_acronym: str) -> int:
        acronyms_list = get_institutes_acronyms()
        if faculty_acronym.lower().replace(' ', '').replace('\n', '') in acronyms_list:
            faculty_id = get_value_by_another_key(key_to_search='abbr',
                                                        value_to_search=faculty_acronym,
                                                        key_to_return_value='id')
            return faculty_id
        else:
            raise WrongInstituteAcronym(faculty_acronym)

    @staticmethod
    def is_valid_group(group_number: str) -> str:
        ...  # Попытка достучаться до страницы расписания по выбранной группе (если есть данные)
        valid_group_number = "5130904/20002"
        return valid_group_number

    def change_faculty(self):
        pass

    def change_group(self):
        pass
"""