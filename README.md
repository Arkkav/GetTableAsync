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
sudo docker build -t get_table_server .
sudo docker build -t get_table_client .
```

Запуск docker контейнера:
```bash
sudo docker run -it --name get_table_server-instance -dp 8000:8000 get_table_server
sudo docker run -it --name get_table_server-instance -dp 8000:8000 --network get_table_net get_table_server

sudo docker run -it --name get_table_client-instance -dp 8000:8000 get_table_client
sudo docker run -it --name get_table_client-instance -dp 8000:8000 --network get_table_net get_table_client
sudo docker run -it --name get_table_client-instance --network get_table_net get_table_client
sudo docker run -it --name get_table_client-instance --network get_table_net get_table_client python3 main.py

sudo docker run -it --name get_table_client-instance -d --network get_table_net \
--mount type=volume,source=client_volume,destination=$(pwd)/volume:/var/www/html/volume \
get_table_client

sudo docker run -it --name get_table_client-instance -d --network get_table_net \
--mount type=bind,source=$(pwd)/volume,destination=/volume \
get_table_client


sudo fuser -k 80/tcp  # если нужно освободить порт

sudo docker network create get_table_net
sudo docker network inspect get_table_net
sudo docker inspect 616d7ab5835c

sudo docker volume ls

sudo docker system prune -a

sudo docker run -it --name get_table_client-instance -d get_table_client
sudo docker run -it --name get_table_client-instance --network="host" get_table_client 
sudo docker-compose up --build

``` 
Docker-compose:
```bash
docker-compose build
#или
docker-compose up --build
sudo docker run -it --name get_table_client-instance get_table_client

sudo docker run -it a187acbec140

sudo docker-compose up --build

sudo docker-compose up


```

Просмотр лога контейнера:
```bash
sudo docker logs a932baeb5588

sudo docker attach 616d7ab5835c
```