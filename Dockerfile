FROM python:3.10-slim-buster

WORKDIR /btrrme

COPY /requirements/requirements.txt /btrrme/requirements/

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements/requirements.txt

COPY . /btrrme


EXPOSE 8000 9000