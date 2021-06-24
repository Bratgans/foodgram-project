FROM python:3.8.10-slim-buster

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./ .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
