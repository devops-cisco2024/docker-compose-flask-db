FROM python:3.9-alpine AS builder
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt 

FROM python:3.9-alpine
RUN pip cache purge
COPY app.py /app/app.pyq
COPY --from=builder /install /usr/local

WORKDIR /app

