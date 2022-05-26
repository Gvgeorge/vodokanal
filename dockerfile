FROM python:3.9-alpine3.15

WORKDIR /vodokanal

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./vdkproject ./vdkproject 