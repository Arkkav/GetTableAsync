## Два асинхронных микросервиса
### Техническое задание
1. написать два микросервиса: клиент и сервер
2. сервер предоставляет REST API с методом GET
   - метод GET позволяет запросить данные с сервера: первые N строк из таблицы
   - таблица на сервере хранится в памяти (pandas), содержимое таблицы на усмотрение кандидата
   - REST API сервера описать, используя swagger
   - сервер логирует поступающие запросы
3. клиент запрашивает данные с сервера (3 раза), логируя ответы и запросы 
   
##### Требования:
   - код микросервисов разрабатывать на Python 
   - для реализации интерфейсов и взаимодействия использовать aiohttp и acyncio
   - сервисы собрать в виде контейнеров на базе ubuntu 
   - клиент и сервер общаются по localhost
   - разработать скрипты запускающие локально контейнеры с заданными параметрами, с просмотром логов

### Основные модули

- Client
    - main.py - основной модуль отправки запросов на сервера
    - Dockerfile, docker-compose.yml - файлы для сборки образа в контейнер docker
    - .env - файл с описанием переменных окружения
    - requirements.txt - список зависимостей
    - client_volume - папка для записи лога из контейнера
- Server
    - main.py - основной модуль обработки запроса и реализации сервера
    - Dockerfile, docker-compose.yml - файлы для сборки образа в контейнер docker
    - .env - файл с описанием переменных окружения
    - requirements.txt - список зависимостей
    - server_volume - папка для записи лога из контейнера
    - openapi.yaml - описание сервера с помощью swagger

### Установка приложения 
```bash
mkdir GetTableAsync
git clone https://github.com/Arkkav/GetTableAsync.git GetTableAsync
cd GetTableAsync
```

### Запуск сервера
```bash
sudo docker-compose -f ./Server/docker-compose.yml up --build -d
sudo docker stop server_server_1
sudo docker start server_server_1
```

### Запуск клиента
```bash
sudo docker-compose -f ./Client/docker-compose.yml up --build -d
sudo docker stop client_client_1
sudo docker start client_client_1
```
### Просмотр логов:
```bash
tail -n 50  ./Client/client_volume/log.log
tail -n 50  ./Server/server_volume/log.log
```
### Пример использования сервера
```bash
curl -X POST http://0.0.0.0:8000/erhhe
curl http://0.0.0.0:8000/?n=100
curl http://0.0.0.0:8000/?n=3
```





Swagger сервера:

https://app.swaggerhub.com/apis-docs/Arkkav/GetTableAsync/1.0.0#/default/findPetsByStatus