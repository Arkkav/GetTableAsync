FROM ubuntu:latest
#ENV DEBUG=true
#ENV SERVER_ADDRESS='localhost'
#ENV SERVER_PORT=8000
#ENV LOGGER_NAME='get_table_server'
#ENV LOG_FILE_NAME='/var/www/html/server_volume/log.log'
#ENV CSV_URL='https://stepik.org/media/attachments/course/4852/StudentsPerformance.csv'





ENV TZ 'Europe/Moscow'
RUN apt-get update \
  && echo $TZ > /etc/timezone \
  && apt-get install -y tzdata \
  && rm /etc/localtime \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata \
  && apt-get clean \
  && apt-get install -y curl python3.9 python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3.9 python \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.9 get-pip.py \
  && pip3 install --upgrade pip \
  && mkdir -p /var/www/html/ \
  && cd /var/www/html/
WORKDIR /var/www/html
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3.9", "main.py"]
