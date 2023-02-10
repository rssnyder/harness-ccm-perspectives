FROM python:slim

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT python3 main.py