import os
from typing import Dict

from django.core.management.base import BaseCommand, CommandError

from ._models import APPS_MODELS, FILE_EXT, PATH, File

MESSAGE_VALUE_ERROR: str = ('В папке {} есть файлы - {}, '
                            'для которых нет таблиц. '
                            'Используйте имена - {}.')
MESSAGE_EXCEPTION: str = ('В таблице {} есть некорректные данные, '
                          'которые никуда не ссылаются. '
                          'Проверьте csv.')
MESSAGE_COMMAND_ERROR: str = ('В папке {} нет файлов для импорта.')


class Command(BaseCommand):
    help = ('Команда для импорта .csv в базу данных. ')

    def handle(self, *args, **options):
        """Распределить таблицы на зависимые и простые,
        Установить в необходимом порядке, для создания related связей.
        Raises:
            Exception: Выйти из цикла, если есть данные,
            которые не могут быть установлены по причине
            полного отсутствия ссылки в related таблицах.
            (Ошибка при заполнении csv оператором)
        """
        files_names = self.files_is_exists_and_file_name_is_done()
        data = self.distribute_files(files_names)
        if len(data['simple']):
            self.save_files_not_related(data['simple'])
        self.save_files_with_related(data['related'])

    def files_is_exists_and_file_name_is_done(self) -> list:
        """Проверяем наличие файлов и корректности их имен.
        Raises:
            CommandError: В папке нет файлов.
            ValueError: Названия некорректны.
        Returns:
            list: Список названий файлов .csv
        """
        files_names: list = [_.replace(FILE_EXT, '') for _ in os.listdir(PATH)
                             if _.endswith(FILE_EXT)]
        if not len(files_names):
            raise CommandError(MESSAGE_COMMAND_ERROR.format(PATH))

        files_name_error = set(files_names).difference(set(APPS_MODELS))
        if len(files_name_error):
            raise ValueError(
                MESSAGE_VALUE_ERROR.format(PATH, files_name_error,
                                           list(APPS_MODELS))
            )
        return files_names

    def distribute_files(self, files_names) -> Dict[str, list]:
        """Распределить файлы по зависимости таблиц на простые и related.
        Args:
            files_names (list): Список всех файлов в папке.
        Returns:
            Dict[str, list]: Словарь с распределенными
            по simple и related именами файлов.
        """
        related_tables = []
        simple_tables = []
        for file_name in files_names:
            file = File(file_name)
            if len(file.get_table_related_fields):
                related_tables.append(file_name)
            else:
                simple_tables.append(file_name)
        return {'simple': simple_tables,
                'related': related_tables}

    def save_files_not_related(self, files_names) -> None:
        """Установка простых таблиц, не имеющих связей.
        Args:
            files_names (list): Cписок файлов для установки.
        """
        for file_name in files_names:
            file = File(file_name)
            file.open_read_save_file_for_simple_table()

    def save_files_with_related(self, related_files) -> None:
        """Установка созависимых таблиц, не имеющих связей.
        Args:
            related_files (list): Список с названиями зависимых таблиц.
        Raises:
            Exception: Таблица не может быть установлена по причине
            ошибки оператора. Не существует данных для связи.
        """
        start_round_flag = True
        while start_round_flag:
            unrecorded_files = []
            for file_name in related_files:
                file = File(file_name)
                unrecorded_files: dict = (
                    file.open_read_save_file_for_ralated_table(
                        unrecorded_files
                    )
                )
            if len(unrecorded_files):
                if related_files == unrecorded_files:
                    raise Exception(MESSAGE_EXCEPTION.format(file))
                related_files = unrecorded_files
                start_round_flag = True
            else:
                start_round_flag = False
