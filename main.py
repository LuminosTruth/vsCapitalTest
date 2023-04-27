import time
from datetime import datetime
import requests
import xml.etree.ElementTree as ETree
from database import DataBase
from configuration.config_generation import config_database, config

connect_database = DataBase(config, config_database)


def send_response():
    """
    Отправляет POST-запрос на указанные URL в файле конфигурации и записывает полученные данные в БД.
    """
    for key, url in config['URL_GET'].items():
        response = requests.post(url)
        if response.status_code == 200:
            if key == "Resource1":
                get = response.text
                root = ETree.fromstring(get)
                date = convert_to_datetime(root.find("date").text)
                data = root.find("data").text
                connect_database.create_operation(data, date)
            if key == "Resource2":
                get = response.json()
                date = convert_to_datetime(get["date"])
                data = get["data"]
                connect_database.create_operation(data, date)
            if key == "Resource3":
                get = response.text.split(" ")
                date = convert_to_datetime(get[0])
                data = get[1]
                connect_database.create_operation(data, date)


def check_date_format(func):
    """
    Декоратор, проверяющий правильность формата даты.
    Формат неверный = исключение.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Неверный формат времени"

    return wrapper


@check_date_format
def convert_to_datetime(date_str):
    """
    Преобразует строку в формате даты/времени в соответствии с форматом указанным в файле конфигурации.
    """
    formats = ["%d-%m-%Y %H:%M", "%Y-%m-%d %H:%M"]
    try:
        timestamp = int(date_str)
        return datetime.fromtimestamp(timestamp).strftime(config["DATETIME_CONVERT_FORMAT"])
    except ValueError:
        pass
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime(config["DATETIME_CONVERT_FORMAT"])
        except ValueError:
            pass
    raise ValueError


try:
    while True:
        try:
            send_response()
        except requests.exceptions.ConnectionError:
            if config["CYCLE_STOP"]:
                print("Ошибка подключения\nВыход из цикла")
                break
            else:
                print("API не отвечает\nПовторная попытка запроса\n")
        time.sleep(config["REQUEST_DELAY"])
except KeyboardInterrupt:
    pass
