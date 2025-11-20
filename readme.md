# Authentication & Authorization System

Учебный backend-проект, реализующий собственную систему регистрации, JWT-аутентификации, управление аккаунтом, кастомные права доступа и минимальную бизнес-логику (посты).

---

## 🚀 Стек технологий

- Python 3.12  
- Django 5  
- Django REST Framework  
- JWT (кастомная реализация)  
- PostgreSQL / SQLite  

---

## 📦 Установка и запуск

```bash
git clone https://github.com/MaksimDyumin/test-tusk-effMob
cd test-tusk-effMob
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python populate_test_data.py # Создание тестовых данных
python manage.py migrate
python manage.py runserver
```

### Креды тестовых пользователей
```bash
admin:    email: admin@example.com, password: admin123
alice:    email: alice@example.com, password: test1234 
bob:      email: bob@example.com, password: test1234 
charlie   email: charlie@example.com, password: test1234 
```

## 🧩 Архитектура проекта
```bash
project/
│
├── auth_api/        # Регистрация, логин, JWT, soft delete
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── authentication.py
│   └── urls.py
│
├── api/             # Бизнес-логика: посты
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
└── project/
    └── settings.py
```
----------------------------------------------------------------------
## 🔐 AUTH API

### ▶️ Регистрация

**POST /auth/register/**
```bash
Body:
{
  "username": "max",
  "email": "max@example.com",
  "password": "12345",
  "confirm_password": "12345"
}
```

### ▶️ Логин (получение JWT)

**POST /auth/login/**
```bash
Body:
{
  "email": "max@example.com",
  "password": "12345",
}

Response:
{
  "token": "<jwt-token>"
}
```

### ▶️  Изменение данных пользователя
**PUT /auth/update/**
```bash
Body:
{
  "username": "newname",
  "email": "new@example.com",
  "password": "newpassword123"
}

Response:
{
  "username": "newname",
  "email": "new@example.com"
}
```

### ▶️  Изменение пароля пользователя
**PUT /auth/change-password/**
```bash
Body:
{
  "old_password": "oldpass123",
  "new_password": "newpass456",
  "confirm_new_password": "newpass456"
}

Response:
{
  "message": "Password updated successfully"
}
```

### ▶️ Изменение аккаунтов админом
**PUT /auth/admin/update-user/2/**
```bash
Body:
{
  "username": "newname",
  "email": "new@example.com",
  "is_admin": true,
  "is_active": true
}
```

### ▶️ Мягкое удаление аккаунта

**DELETE /auth/delete/**

Деактивирует пользователя (is_active=False).
После деактивации пользователь не может повторно войти.
```bash
Response:
{
  "message": "Account deactivated"
}
```

## 📝 Posts API

### ▶️ Получение постов
**GET /api/posts/**

```bash
Response:
[
  {
      "id": 1,
      "title": "Hello World",
      "text": "Пример текста поста пользователя alice",
      "user": 2
  },
]
```
- Админ: получает все посты

- Пользователь: только свои

### ▶️ Создание постов 
**POST /api/posts/**
```bash
Body:
{
  "title": "My Post",
  "text": "Text"
}
```

### ▶️ Получение поста по id

**GET /api/posts/\<id>**
```bash
Body:
{
  "id": 1,
  "title": "My Post",
  "text": "Text",
  "user": 1 # id пользователя
}
```
- Админ: доступ ко всем постам

- Автор поста: доступ к своему посту

- Другие пользователи: 403 Forbidden

### ▶️ Изменение поста
**PUT /api/posts/\<id>/**
```bash
Body:
{
  "title": "Updated Title",
  "text": "Updated text"
}
```
- Изменяет пост

- Доступ: админ или автор поста

- Body пример:

## 🔒 Авторизация и Permissions

Проект использует кастомный JWT:
```bash
Authorization: Bearer <jwt-token>
```

Основные permissions:
```bash
IsAuthenticated — доступ только авторизованным

IsAdminOrOwner — доступ к посту только админу или владельцу
```
## 📝 Описание таблиц
```bash
| Поле       | Тип          | Описание                              |
| ---------- | ------------ | ------------------------------------- |
| id         | Integer (PK) | Уникальный идентификатор пользователя |
| username   | varchar(100) | Имя пользователя                      |
| email      | varchar      | Email, уникальный                     |
| firstname  | varchar(50)  | Имя                                   |
| lastname   | varchar(50)  | Фамилия                               |
| middlename | varchar(50)  | Отчество                              |
| password   | varchar(150) | Хэш пароля                            |
| is_admin   | boolean      | Флаг администратора (True/False)      |
| is_active  | boolean      | Активен ли аккаунт (soft delete)      |
```

```bash
| Поле    | Тип                             | Описание                       |
| ------- | ------------------------------- | ------------------------------ |
| id      | Integer (PK)                    | Уникальный идентификатор поста |
| title   | varchar(50)                     | Заголовок поста                |
| text    | text                            | Текст поста                    |
| user_id | Integer (FK → auth_api_user.id) | Владелец поста (ForeignKey)    |
```

🔗 Связи
```bash
auth_api_user
    1 ──< api_posts.user_id
```
- Один пользователь → может иметь много постов (related_name='posts').

- Каждый пост → принадлежит одному пользователю.

## 📝 Метод тестирования

**JWT** авторизация не прокинута в **Django** по этому рекомендуется использовать **Postman**.
