pattern = {
    'monday': [],
    'tuesday': [],
    'wednesday': [],
    'thursday': [],
    'friday': [],
    'saturday': []
    }

dow2dow = {
    'Понедельник': 'monday',
    'Вторник': 'tuesday',
    'Среда': 'wednesday',
    'Четверг': 'thursday',
    'Пятница': 'friday',
    'Суббота': 'saturday'
    }

subj = [
    'МАТ', 'ЛИТ', 'ГЕО', 'ИСТ',
    'ХИМ', 'РУС. ЯЗ', 'ИСТОРИЯ', 'ОБЖ',
    'ИНФ', 'ФИЗ', 'ОБЩ', 'МАТ Л', 'БИО', 'ФИЗ Л'
    ]

full_subj_name = {
    'МАТ': 'Математика',
    'ЛИТ': 'Литература',
    'ГЕО': 'Геометрия',
    'ИСТ': 'История',
    'ХИМ': 'Химия',
    'РУС. ЯЗ': 'Русский язык',
    'ИСТОРИЯ': 'История',
    'БИО': 'Биология',
    'ЛИТРА': 'Литература',
    'ОБЖ': 'ОБЖ',
    'ИНФ': 'Информатика',
    'ФИЗ': 'Физика',
    'ОБЩ': 'Обществознание',
    'МАТ Л': 'Лекция по математике',
    'ФИЗ Л': 'Лекция по физике'
    }


class ScheduleProperties:
    bug_rows: list[int]
    useless_columns: list[int]
    useless_rows: list[int]
    last_row: list[int]
    second_time: bool

    def __init__(self, _bug_rows, _useless_columns, _useless_rows, _last_row, _second_time):
        self.bug_rows = _bug_rows
        self.useless_columns = _useless_columns
        self.useless_rows = _useless_rows
        self.last_row = _last_row
        self.second_time = _second_time


first_table_properties = ScheduleProperties([22, 34, 37, 67], [1, 24, 41], [15, 27, 38, 51, 64, 76], 75, True)
second_table_properties = ScheduleProperties([], [1, 23, 40], [17, 18, 33, 34, 49, 50, 65, 66, 81, 82], 96, False)


def validate_str(__s):
    return str(__s).strip('_').replace('.0', '').rstrip('_')


def get_merged_cell_val(sheet, __cell):
    rng = [s for s in sheet.merged_cells.ranges if __cell.coordinate in s]
    return sheet.cell(rng[0].min_row, rng[0].min_col).value if len(rng) != 0 else __cell.value
