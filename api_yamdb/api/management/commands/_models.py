import contextlib
import csv
import os
from typing import Dict, List

from django.apps import apps

PATH: str = os.path.join('static', 'data')
FILE_EXT: str = '.csv'
APPS_MODELS: dict = {model.__name__.lower(): model
                     for model in apps.get_models(include_auto_created=True)}


def change_key_name(key):
    """Подменить значение ключа для user."""
    name = ['author', 'user']
    try:
        name.remove(key)
    except ValueError:
        return key
    return name[0]


class File():
    """Файл csv для записи в таблицу."""
    MESSAGE_TYPE_ERROR: str = ('Назование столбца таблицы {} '
                               'отличается. Используйте {}.')
    MESSAGE_SUCCESS: str = ('Данные файла {}.csv успешно занесены в базу. '
                            'Заполнено {} строк.')

    def __init__(self, file_name) -> None:
        self.file_name = file_name

    @property
    def get_file_path(self) -> str:
        """Получить путь до файла.
        """
        return os.path.join(PATH, self.file_name + FILE_EXT)

    @property
    def get_table(self) -> object:
        """Получить объект модели таблицы по имени файла.
        """
        return APPS_MODELS[self.file_name]

    @property
    def get_table_all_fields(self) -> List[str]:
        """Получить все поля таблицы. Информационно.
        """
        table_model = self.get_table
        return [f.name for f in table_model._meta.fields]

    @property
    def get_table_related_fields(self) -> List[str]:
        """Получить список полей таблицы с полем типа ForeigenKey.
        """
        table_model = self.get_table
        return [f.name for f in table_model._meta.fields
                if f.__class__.__name__ == 'ForeignKey']

    def open_read_save_file_for_simple_table(self) -> List[str]:
        """Открыть файл и записать его в таблицу без связей.
        """
        with open(self.get_file_path, 'r', encoding="utf-8") as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            field_name = next(rows)
            count = self.save_by_simple_rows(rows, field_name)
            print(self.MESSAGE_SUCCESS.format(self.file_name, count))

    def open_read_save_file_for_ralated_table(self,
                                              unrecorded_files
                                              ) -> List[str]:
        """Открыть файл и записать его в таблицу
        Args:
            unrecorded_files (list): Пустой список
        Returns:
            List[str]: Список файлов, которые не были записаны в таблицы.
        """
        with open(self.get_file_path, 'r', encoding="utf-8") as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            field_name = next(rows)
            data = self.save_by_related_rows(rows, field_name)
            check_recorded_row = data['check']
            if False not in check_recorded_row:
                print(self.MESSAGE_SUCCESS.format(self.file_name,
                                                  data['row_done']))
            else:
                unrecorded_files.append(self.file_name)
        return unrecorded_files

    def save_by_simple_rows(self, rows, field_name) -> dict:
        """Построчная запись в таблицу.
        Raises:
            TypeError: В csv есть столбец,
            название которого не совпадает с табличными столбцами.
        Returns:
            List[bool]: Контрольный список - удачно ли прошла запись строки.
        """
        count = 0
        for row in rows:
            values_for_save: Dict[str, str] = dict(zip(field_name, row))
            try:
                data = self.get_table(**values_for_save)
            except ValueError:
                pass
            except TypeError as e:
                raise TypeError(self.MESSAGE_TYPE_ERROR.format(
                    self.file_name,
                    self.get_table_all_fields
                )) from e
            data.save()
            count += 1
        return count

    def save_by_related_rows(self, rows, field_name) -> dict:
        """Построчная запись в таблицу.
        Raises:
            TypeError: В csv есть столбец,
            название которого не совпадает с табличными столбцами.
        Returns:
            List[bool]: Контрольный список - удачно ли прошла запись строки.
        """
        check_recorded_row = []
        count = 0
        for row in rows:
            record_flag = True
            values_for_save = (
                self.save_by_rows_related_from_another_table(
                    dict(zip(field_name, row))
                )
            )
            try:
                data = self.get_table(**values_for_save)
            except ValueError:
                pass
            except TypeError as e:
                raise TypeError(self.MESSAGE_TYPE_ERROR.format(
                    self.file_name,
                    self.get_table_all_fields
                )) from e
            try:
                data.save()
                count += 1
            except Exception:
                record_flag = False
            check_recorded_row.append(record_flag)
            data = {
                'check': check_recorded_row,
                'row_done': count
            }
        return data

    def save_by_rows_related_from_another_table(self,
                                                values_for_save
                                                ) -> Dict[str, object]:
        """Построчная запись в таблицу для таблиц с related_field
        Args:
            values_for_save (_type_): Данные,
            которые не имеют ссылочных объектов.
        Returns:
            Dict[str, object]: Измененные данные,
            в которых вместо строки объект.
        """
        for key, value in values_for_save.items():
            if key in self.get_table_related_fields:
                key = change_key_name(key)
                table_related = APPS_MODELS[key]
                with contextlib.suppress(table_related.DoesNotExist):
                    value = table_related.objects.get(id=value)
                key = change_key_name(key)
            values_for_save[key] = value
        return values_for_save

    def __str__(self) -> str:
        return self.file_name
