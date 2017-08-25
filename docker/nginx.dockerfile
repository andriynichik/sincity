FROM nginx:1.12.1-alpine

COPY ./config/nginx /etc/nginx

RUN apt-get update -y

RUN apt-get install -y git

WORKDIR /app

RUN git clone https://github.com/bpteam/WebCrawler_FR.git .