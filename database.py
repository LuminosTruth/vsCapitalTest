import sys
import psycopg2
from datetime import datetime
import requests


class DataBase:
    def __init__(self, config, config_database):
        """
        Инициализация класса и соединение с базой данных.

        Аргументы:
        config -- словарь с конфигурацией
        config_database -- словарь с конфигурацией базы данных
        """
        self.counter = 0
        self.counter_date = datetime.utcnow().date()
        self.config = config
        self.config_database = config_database
        try:
            self.connect = psycopg2.connect(**self.config_database)
        except psycopg2.OperationalError:
            print("Неудачное подключение к базе данных, проверьте файл конфигурации (config_database.json)")
            sys.exit(1)

        self.cursor = self.connect.cursor()

    def create_operation(self, number: float, date: datetime):
        """
        Создание операции в базе данных.

        Аргументы:
        number -- номер операции
        date -- дата операции
        """
        if self.operation_is_exist(number, date) is not True:
            self.cursor.execute(f"INSERT INTO operations VALUES (%s, %s)", (number, date))
            self.connect.commit()
            self.counter += 1
            if self.counter_date != datetime.utcnow().date():
                self.send_post_to_api()
            if self.counter >= self.config["REQUEST_COUNT"]:
                self.send_post_to_api()

    def operation_is_exist(self, number: float, date: datetime):
        """
        Проверка на существование операции в базе данных.

        Аргументы:
        number -- число
        date -- дата

        Возвращает True, если операция существует в базе данных, иначе - False.
        """
        self.cursor.execute(f"SELECT * FROM operations WHERE number = %s AND date = %s", (number, date))
        if self.cursor.fetchone():
            return True
        else:
            return False

    def send_post_to_api(self):
        """
        Отправка POST запроса на API.

        Запрос содержит информацию о количестве операций за период времени.

        date_start : Начало итерации
        date_end : Конец итерации
        count : Количество итераций
        """
        time_start = self.counter_date
        time_end = datetime.utcnow().date()
        convert_time_start = time_start.strftime(self.config["DATETIME_CONVERT_FORMAT"])
        convert_time_end = time_end.strftime(self.config["DATETIME_CONVERT_FORMAT"])
        response = requests.post(self.config["URL_POST"], json=
        {
            "date_start": convert_time_start,
            "date_end": convert_time_end,
            "count": self.counter
        })
        if response.status_code == 200:
            self.counter = 0
