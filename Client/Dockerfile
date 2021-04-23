FROM ubuntu:latest
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
