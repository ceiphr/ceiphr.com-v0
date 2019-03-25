FROM ubuntu:18.04
WORKDIR /usr/src/app
COPY / requirements.txt ./
RUN apt update && apt install python &&\
    pip install --no-cache-dir -r requirements.txt &&\
    apt install node && npm -i sass
EXPOSE 8000
CMD gunicorn ceiphrcom.wsgi:application --bind 0.0.0.0:8000 --workers 3