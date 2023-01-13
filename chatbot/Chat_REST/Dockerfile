# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install numpy
RUN pip3 install tensorflow
RUN pip3 install flask
RUN pip3 install flask-cors
RUN pip3 install nltk
RUN pip3 install psycopg2-binary

COPY . .

EXPOSE 5000

CMD [ "python3", "ChatAPI.py"]