# QnA Project

Краткое описание
- Веб-приложение "Вопрос-Ответ" (Q&A): пользователи могут задавать вопросы и давать ответы.

Технологии
- Python 3.8+
- Django 5.0+
- Django REST Framework
- PostgreSQL
- Docker, Docker Compose

Запуск в локальной среде через Docker

1) Запуск с помощью docker-compose
- Собрать и запустить контейнеры:
  ```text
  docker-compose up --build -d
  ```
- Выполнить миграции:
  ```text
  docker-compose run web python manage.py migrate
  ```
- Просмотреть логи (если необходимо):
  ```text
  docker-compose logs -f
  ```

2) Проект будет доступен по адресу:
```text
  http://localhost:8000
```
3) Проведение тестов:
```text
   docker-compose run web pytest
```

   


