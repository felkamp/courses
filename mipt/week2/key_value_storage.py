# На этой неделе мы с вами реализуем собственный key-value storage.
# Вашей задачей будет написать скрипт, который принимает в качестве
# аргументов ключи и значения и выводит информацию из хранилища
# (в нашем случае — из файла).
# Запись значения по ключу
# > storage.py --key key_name --val value

# Получение значения по ключу
# > storage.py --key key_name

# Ответом в данном случае будет вывод с помощью print соответствующего значения
# > value
# или
# > value_1, value_2

# если значений по этому ключу было записано несколько. Метрики сохраняйте в порядке их добавления.
# Обратите внимание на пробел после запятой.
# Если значений по ключу не было найдено, выводите пустую строку или None.
# Для работы с аргументами командной строки используйте модуль argparse.
# Вашей задачей будет считать аргументы, переданные вашей программе,
# и записать соответствующую пару ключ-значение в файл хранилища
# или вывести значения, если был передан только ключ.
# Хранить данные вы можете в формате JSON с помощью стандартного модуля json.
# Проверьте добавление нескольких ключей и разных значений.
# Файл следует создавать с помощью модуля tempfile.

import tempfile
import os
import argparse
import json


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    parser.add_argument('--value')
    args = parser.parse_args()
    return args


def get_data(storage_path):
    data = {}
    with open(storage_path, 'a+') as f:
        f.seek(0)
        try:
            data = json.load(f)
        except:
            pass
    return data


def save(key, value):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    data = get_data(storage_path)
    with open(storage_path, 'w') as f:
        if key in data:
            data[key].append(value)
        else:
            data[key] = [value]
        json.dump(data, f)


def print_values(key):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    data = get_data(storage_path)
    print(', '.join(data.get(key, [])))


def process_storage():
    kwargs = parse()
    if kwargs.key is not None and kwargs.value is None:
        print_values(kwargs.key)
    elif kwargs.key is not None and kwargs.value is not None:
        save(kwargs.key, kwargs.value)


if __name__ == '__main__':
    process_storage()
