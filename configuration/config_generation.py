import json
import os

app_path = os.getcwd() + "/configuration"

"""
URL_GET - Список URL ресурсов для запросов
URL_POST - URL для отправки POST запроса в API при достижении {REQUEST_COUNT}
DATETIME_CONVERT_FORMAT - Формат времени в который форматируется все обрабатываемые datetime
REQUEST_DELAY - Задержка между каждыми 3 запросами к API
REQUEST_COUNT - При достижении данного кол-ва сбрасывается счётчик и отправляется POST запрос в API с временем события
CYCLE_STOP - True: при неудачном запросе к API цикл останавливается. False: запросы продолжат поступать|
DEBUG - True: выводит некоторые сообщения об исключениях
"""

config = {
    "URL_GET": {
        "Resource1": "http://127.0.0.1:8000/operations/resource/1",
        "Resource2": "http://127.0.0.1:8000/operations/resource/2",
        "Resource3": "http://127.0.0.1:8000/operations/resource/3"},
    "URL_POST": "http://127.0.0.1:8000/operations/resource/post/",
    "DATETIME_CONVERT_FORMAT": "%d-%m-%Y %H:%M",
    "REQUEST_DELAY": 1,
    "REQUEST_COUNT": 9,
    "CYCLE_STOP": False,
    "DEBUG": True
}

config_database = {
    "host": "localhost",
    "port": 5432,
    "database": "vsCapital",
    "user": "postgres",
    "password": "JAJetA200333"
}

if os.path.isfile(f"{app_path}/config.json"):
    with open(f"{app_path}/config.json", "r") as file:
        config = json.load(file)
else:
    with open(f"{app_path}/config.json", "w") as file:
        json.dump(config, file, indent=4)

if os.path.isfile(f"{app_path}/config_database.json"):
    with open(f"{app_path}/config_database.json", "r") as file:
        config_database = json.load(file)
else:
    with open(f"{app_path}/config_database.json", "w") as file:
        json.dump(config_database, file, indent=4)
