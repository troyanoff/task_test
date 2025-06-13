FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY src/models/ models/
COPY src/core/ core/
COPY src/sync_tasks/ sync_tasks/
COPY src/task_schemas/ schemas/
COPY src/sync_worker/ .
       