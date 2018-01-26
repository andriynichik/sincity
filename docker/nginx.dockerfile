FROM nginx:1.12.1

COPY ./config/nginx /etc/nginx

WORKDIR /app