FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./korzh_bot/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./korzh_bot/ .

