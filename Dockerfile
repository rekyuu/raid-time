FROM python:3.11.9-alpine AS base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w", "1", "-b", "0.0.0.0", "app:create_app()" ]