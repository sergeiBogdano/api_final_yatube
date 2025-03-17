Yatube API Final Project
Описание
Данный проект представляет собой API для социальной сети Yatube. API обеспечивает возможность:

Просмотра публикаций и комментариев.
Управления подписками между пользователями (подписка/отписка).
Аутентификации пользователей с помощью JWT-токенов.
Проект создан для обеспечения гибкого и масштабируемого backend-решения, позволяющего пользователям обмениваться контентом и взаимодействовать друг с другом через REST API.

Функционал
Публикации и комментарии:
Позволяет пользователям просматривать публикации, детальную информацию о публикациях и комментарии к ним.

Подписки (Follow):

GET /follow/ — возвращает список подписок текущего пользователя с поддержкой поиска по параметру search.
POST /follow/ — создает подписку текущего пользователя на другого пользователя. Если попытаться подписаться на самого себя или повторно — возвращается ошибка.
Аутентификация (JWT):

POST /api/v1/auth/jwt/create/ — получение JWT-токена (refresh и access).
POST /api/v1/auth/jwt/refresh/ — обновление access-токена.
POST /api/v1/auth/jwt/verify/ — верификация токена.
Технологический стек
Python 3.x
Django — основной веб-фреймворк.
Django REST Framework (DRF) — создание REST API.
SimpleJWT — работа с JWT-токенами.
Djoser — упрощение управления пользователями (регистрация, смена пароля и т.д.).
SQLite — база данных по умолчанию (рекомендуется использовать PostgreSQL для продакшена).
Redoc — генерация документации API.
Развертывание
Предварительные требования
Python 3.x
pip
Инструкция по развертыванию
Клонирование репозитория:

bash
Копировать
Редактировать
git clone <URL репозитория>
cd api_final_yatube
Создание и активация виртуального окружения:

bash
Копировать
Редактировать
python -m venv venv
# Для Linux/macOS:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate
Установка зависимостей:

bash
Копировать
Редактировать
pip install -r requirements.txt
Применение миграций:

bash
Копировать
Редактировать
python manage.py migrate
Запуск сервера:

bash
Копировать
Редактировать
python manage.py runserver
Проверка документации API: Откройте браузер и перейдите по адресу: http://127.0.0.1:8000/redoc/

Пример запроса и ответа
Получение JWT-токена
Запрос:

bash
Копировать
Редактировать
POST /api/v1/auth/jwt/create/
Content-Type: application/json

{
  "username": "TestUser",
  "password": "1234567"
}
Ответ:

json
Копировать
Редактировать
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
Получение списка подписок
Запрос:

bash
Копировать
Редактировать
GET /api/v1/follow/
Authorization: Bearer <access_token>
Ответ (пример):

json
Копировать
Редактировать
[
  {
    "user": "TestUser",
    "following": "AnotherUser"
  },
  {
    "user": "TestUser",
    "following": "SomeOtherUser"
  }
]
Автор
Сергей Богданов
GitHub: github.com/sergeibogdanov
