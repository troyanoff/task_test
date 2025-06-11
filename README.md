# task_test



### Запуск проекта

- Для запуска проекта создайте файл .env и скопируйте в него все из
     .env-example ```cp .env-example .env```

- После чего командой ```sudo docker-compose up -d``` запустите проект


### Запуск тестов

- Установите виртуальное окружение ```python3 -m venv venv```
- Активируйте его ```. venv/bin/activate```
- Установите необходимые зависимости ```pip install -r requirements-tests.txt```
- Запустите тесты ```pytest```

### Ссылки

- [Документация сервиса](http://localhost/api/docs)
