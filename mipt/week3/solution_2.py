# Предположим есть данные о разных автомобилях и спецтехнике.
# Данные представлены в виде таблицы с характеристиками.
# Вся техника разделена на три вида: спецтехника, легковые
# и грузовые автомобили. Обратите внимание на то, что некоторые
# характеристики присущи только определенному виду техники.
# Например, у легковых автомобилей есть характеристика
# «кол-во пассажирских мест», а у грузовых автомобилей
# — габариты кузова: «длина», «ширина» и «высота».

# Вам необходимо создать свою иерархию классов для данных,
# которые описаны в таблице. Классы должны называться
# CarBase (базовый класс для всех типов машин),
# Car (легковые автомобили),
# Truck (грузовые автомобили)
# и SpecMachine (спецтехника).
# Все объекты имеют обязательные атрибуты:
# - car_type, значение типа объекта и может принимать одно из значений: «car», «truck», «spec_machine».
# - photo_file_name, имя файла с изображением машины,
# допустимы названия файлов изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»
# - brand, марка производителя машины
# - carrying, грузоподъемность

# В базовом классе CarBase нужно реализовать
# метод get_photo_file_ext для получения расширения файла изображения.
# Расширение файла можно получить при помощи os.path.splitext.
#
# Для грузового автомобиля необходимо в конструкторе
# класса определить атрибуты: body_length, body_width,
# body_height, отвечающие соответственно за габариты кузова —
# длину, ширину и высоту. Габариты передаются в параметре
# body_whl (строка, в которой размеры разделены латинской буквой «x»).
# Обратите внимание на то, что характеристики кузова должны быть
# вещественными числами и характеристики кузова могут быть не
# валидными (например, пустая строка). В таком случае всем
# атрибутам, отвечающим за габариты кузова, присваивается значение равное нулю.
#
# Также для класса грузового автомобиля необходимо
# реализовать метод get_body_volume, возвращающий объем кузова.
#
# В классе Car должен быть определен
# атрибут passenger_seats_count (количество пассажирских мест),
# а в классе SpecMachine — extra (дополнительное описание машины)

# Далее вам необходимо реализовать функцию get_car_list,
# на вход которой подается имя файла в формате csv.
# Файл содержит данные, аналогичные строкам из таблицы.
# Вам необходимо прочитать этот файл построчно при помощи
# модуля стандартной библиотеки csv. Затем проанализировать
# строки на валидность и создать список объектов
# с автомобилями и специальной техникой. Функция
# должна возвращать список объектов.

# Первая строка в исходном файле — это заголовок csv, который
# содержит имена колонок. Нужно пропустить первую строку из
# исходного файла. Обратите внимание на то, что в некоторых
# строках исходного файла , данные могут быть заполнены некорректно,
# например, отсутствовать обязательные поля или иметь не валидное
# значение. В таком случае нужно проигнорировать подобные строки
# и не создавать объекты. Строки с пустым или не валидным значением
# для body_whl игнорироваться не должны.  Вы можете использовать
# стандартный механизм обработки исключений в процессе чтения,
# валидации и создания объектов из строк csv-файла. Проверьте
# работу вашего кода с входным файлом, прежде чем загружать
# задание для оценки.

import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        root_ext = os.path.splitext(self.photo_file_name)
        return root_ext[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        attrs = ['body_length', 'body_width', 'body_height']
        try:
            params = body_whl.split('x')
            for index, value in enumerate(params):
                setattr(self, attrs[index], float(value))
        except (ValueError, IndexError, AttributeError):
            for attr in attrs:
                setattr(self, attr, 0.0)
        super().__init__(brand, photo_file_name, carrying)

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def csv_is_valid(**kwargs):
    car_type = kwargs.get('car_type')
    brand = kwargs.get('brand')
    photo_file_name = kwargs.get('photo_file_name')
    try:
        float(kwargs.get('carrying'))
    except (ValueError, TypeError):
        return False
    if car_type not in {'car', 'truck', 'spec_machine'} or not brand or os.path.splitext(photo_file_name)[1] not in {
        '.jpg', '.jpeg', '.png', '.gif'}:
        return False

    if car_type == 'spec_machine' and not kwargs.get('extra'):
        return False

    if car_type == 'car':
        try:
            int(kwargs.get('passenger_seats_count'))
        except (ValueError, TypeError):
            return False

    return True


def create_obj(attrs):
    car_type = attrs.pop('car_type', None)
    if car_type == 'car':
        attrs.pop('extra', None)
        attrs.pop('body_whl', None)
        return Car(**attrs)
    elif car_type == 'spec_machine':
        attrs.pop('passenger_seats_count', None)
        attrs.pop('body_whl', None)
        return SpecMachine(**attrs)
    elif car_type == 'truck':
        attrs.pop('passenger_seats_count', None)
        attrs.pop('extra', None)
        return Truck(**attrs)


def get_car_list(csv_filename):
    car_list = []
    keys = ['car_type', 'brand', 'passenger_seats_count', 'photo_file_name',
            'body_whl', 'carrying', 'extra']

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            attrs = {key: value for key, value in zip(keys, row)}
            if csv_is_valid(**attrs):
                car_list.append(create_obj(attrs))
    return car_list
