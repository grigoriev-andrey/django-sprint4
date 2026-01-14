# django_sprint4

Учебный проект блога на Django: поддерживаются публикации, категории, комментарии, профили,
авторизация и пагинация. Поддерживает загрузку изображений и статические
страницы.

## Требования

- Python 3.10+
- Django 5.1+
- pip

## Установка

python -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
python blogicum/manage.py migrate
python blogicum/manage.py loaddata db.json

## Запуск

python blogicum/manage.py runserver

Откройте `http://127.0.0.1:8000/`.

## Тесты

pytest

## Структура проекта

- `blogicum/blog` - публикации, категории, комментарии, пагинация, профили
- `blogicum/users` - регистрация и редактирование профиля
- `blogicum/pages` - статические страницы и кастомные обработчики ошибок
- `templates` - шаблоны для фронта 
- `db.json` - фикстуры
