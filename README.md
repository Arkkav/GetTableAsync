#### 1. написать два микросервиса: клиент и сервер

#### 2. сервер предоставляет REST API с методом GET
   - метод GET позволяет запросить данные с сервера: первые N строк из таблицы
   - таблица на сервере хранится в памяти (pandas), содержимое таблицы на усмотрение кандидата
   - REST API сервера описать, используя swagger
   - сервер логирует поступающие запросы
  
#### 3. клиент запрашивает данные с сервера (3 раза), логируя ответы и запросы

####  Требования:
   - код микросервисов разрабатывать на Python 
   - для реализации интерфейсов и взаимодействия использовать aiohttp и acyncio
   - сервисы собрать в виде контейнеров на базе ubuntu 
   - клиент и сервер общаются по localhost
   - разработать скрипты запускающие локально контейнеры с заданными параметрами, с просмотром логов



Запуск скрипта из командной строки:
```bash
apt install python3.9-venv
python3.9 -m venv venv
. venv/bin/activate
/home/arkkav/projects/GetTableAsync/Client/venv/bin/python3.9 -m pip install --upgrade pip
pip install -r requirements.txt
python3.9 -m aiohttp.web -H localhost -P 8000 main:web_app
```

```bash
gunicorn main:web_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```
Просмотр лога:
```bash
tail ...
```

```bash
sudo docker build -t get_table_async .
```

Запуск docker контейнера:
```bash
#sudo docker run --rm -it --name get_table_async-instance -p 8000:8000 get_table_async
#sudo fuser -k 80/tcp  # если нужно освободить порт

``` 