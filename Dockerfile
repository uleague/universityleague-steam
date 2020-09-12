FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./korzh_bot/ ./korzh_bot/

ENV PORT=80
EXPOSE 80

RUN mkdir -p log

CMD ["python", "-m", "korzh_bot"]