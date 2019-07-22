FROM python:3.7.4

RUN apt-get update && apt-get install -y postgresql

COPY . /app/

WORKDIR /app

RUN pip install -r /app/requirements.txt
