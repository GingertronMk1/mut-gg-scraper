FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    util-linux

RUN pip install \
    lxml \
    requests

