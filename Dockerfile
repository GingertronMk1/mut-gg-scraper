FROM python:3.12-alpine

WORKDIR /app

RUN pip install \
    lxml \
    requests