FROM ubuntu:latest
MAINTAINER fnndsc "dev@babymri.org"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && mkdir -p /var/www/html/ \
  && cd /var/www/html/
WORKDIR /var/www/html
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "aiohttp.web", "-H", "0.0.0.0", "-P", "8000", "main:web_app"]