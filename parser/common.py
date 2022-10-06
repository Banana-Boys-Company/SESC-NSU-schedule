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
    'ИНФ', 'ФИЗ', 'ОБЩ', 'МАТ Л', 'БИО'
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
    'МАТ Л': 'Лекция по математике'
    }

bug_rows = [22, 34, 37, 67]


def validate_str(__s):
    return str(__s).rstrip('_').replace('.0', '')


def get_merged_cell_val(sheet, __cell):
    rng = [s for s in sheet.merged_cells.ranges if __cell.coordinate in s]
    return sheet.cell(rng[0].min_row, rng[0].min_col).value if len(rng) != 0 else __cell.value
