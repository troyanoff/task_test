#!/usr/bin/env bash

while ! nc -z $SERVICE_HOST $SERVICE_PORT; do
      sleep 0.1
      echo "wait service"
done 


python3 truncate_tables.py
python3 create_superuser.py
pytest
# python3 truncate_tables.py