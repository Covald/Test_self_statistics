FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d
WORKDIR /code
COPY ./certs/ssl/testFNS.pem ./certs/ssl/device.key ./certs/