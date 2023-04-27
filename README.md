# Тестовое задание для компании "ВС Кэпитал"

##### Конфигурация приложения :
###### URL_GET - Список URL ресурсов для запросов
###### URL_POST - URL для отправки POST запроса в API при достижении {REQUEST_COUNT}
###### DATETIME_CONVERT_FORMAT - Формат времени в который форматируется все обрабатываемые datetime
###### REQUEST_DELAY - Задержка между каждыми 3 запросами к API
###### REQUEST_COUNT - При достижении данного кол-ва сбрасывается счётчик и отправляется POST запрос в API с временем события
###### CYCLE_STOP - True: при неудачном запросе к API цикл останавливается. False: запросы продолжат поступать


```
config = {
    "URL_GET": {
        "Resource1": "http://127.0.0.1:8000/operations/resource/1",
        "Resource2": "http://127.0.0.1:8000/operations/resource/2",
        "Resource3": "http://127.0.0.1:8000/operations/resource/3"},
    "URL_POST": "http://127.0.0.1:8000/operations/resource/post/",
    "DATETIME_CONVERT_FORMAT": "%d-%m-%Y %H:%M",
    "REQUEST_DELAY": 1,
    "REQUEST_COUNT": 1000,
    "CYCLE_STOP": False
}
```

####
