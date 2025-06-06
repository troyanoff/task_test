FROM python:3.12-slim

WORKDIR /functional

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir \
    && apt update\
    && apt install netcat-traditional

COPY ./functional .

EXPOSE 9001

ENTRYPOINT ["sh", "run_test.sh"]
       