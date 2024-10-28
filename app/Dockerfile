FROM python:3.10-slim

COPY ../requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
