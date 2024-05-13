FROM python:alpine AS builder
COPY requirements.txt .
RUN apk update && \
    apk add gcc musl-dev mariadb-connector-c-dev && \
    pip install --prefix=/temp -r requirements.txt 

FROM python:alpine
RUN apk update && \ 
    apk add mariadb-connector-c-dev
COPY app.py databasefunctions.py secretsfile.py /app/
COPY /templates   /app/templates
COPY /static   /app/static
COPY --from=builder /temp /usr/local

WORKDIR /app

