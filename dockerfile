FROM python:3.9-alpine3.15

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python -m pip install django-cors-headers

COPY ./vdkproject ./vdkproject 

RUN chmod +x /vdkproject/start.sh

WORKDIR /vdkproject

