FROM python:3.8.13
WORKDIR /app

RUN apt-get update && apt-get -y install cron

COPY . .

RUN pip install -r requirements.txt

CMD python /app/main.py