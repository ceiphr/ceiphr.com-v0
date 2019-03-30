# TODO This is BROKEN ATM, don't use.
FROM python:3
WORKDIR /usr/src/app
COPY / requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
EXPOSE 8000
CMD gunicorn ceiphrcom.wsgi:application --bind 0.0.0.0:8000 --workers 3