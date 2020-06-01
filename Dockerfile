FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /gk-lk

WORKDIR /gk-lk

ADD . /gk-lk/

RUN pip install -r req.txt