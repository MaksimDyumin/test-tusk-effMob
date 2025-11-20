import os
import django
import random

# Установим настройки Django (замени 'myproject' на свою папку проекта)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_tusk_effmob.settings")
django.setup()

from auth_api.models import User
from api.models import Posts
from django.contrib.auth.hashers import make_password

# ----------------------------
# Создание пользователей
# ----------------------------
def create_users():
    print("Создаём пользователей...")

    # Админ
    admin, created = User.objects.get_or_create(
        email="admin@example.com",
        defaults={
            "username": "admin",
            "firstname": "Admin",
            "lastname": "User",
            "middlename": "",
            "password": make_password("admin123"),
            "is_admin": True,
            "is_active": True,
        }
    )
    if created:
        print(f"Создан админ: {admin.email}")

    # Обычные пользователи
    users_data = [
        {"username": "alice", "email": "alice@example.com", "firstname": "Alice", "lastname": "Smith"},
        {"username": "bob", "email": "bob@example.com", "firstname": "Bob", "lastname": "Johnson"},
        {"username": "charlie", "email": "charlie@example.com", "firstname": "Charlie", "lastname": "Brown"},
    ]

    users = []
    for udata in users_data:
        user, created = User.objects.get_or_create(
            email=udata["email"],
            defaults={
                "username": udata["username"],
                "firstname": udata["firstname"],
                "lastname": udata["lastname"],
                "middlename": "",
                "password": make_password("test1234"),
                "is_admin": False,
                "is_active": True,
            }
        )
        if created:
            print(f"Создан пользователь: {user.email}")
        users.append(user)

    return admin, users

# ----------------------------
# Мягкое удаление одного пользователя
# ----------------------------
def soft_delete_user(users, username_to_delete="bob"):
    print(f"Мягкое удаление пользователя '{username_to_delete}'...")
    user = next((u for u in users if u.username == username_to_delete), None)
    if user:
        user.is_active = False
        user.save()
        print(f"Пользователь {username_to_delete} деактивирован.")
    else:
        print(f"Пользователь {username_to_delete} не найден.")

# ----------------------------
# Создание постов
# ----------------------------
def create_posts(users, admin):
    print("Создаём посты...")

    sample_titles = [
        "Hello World",
        "My First Post",
        "Django Tips",
        "REST API Guide",
        "Testing JWT",
        "Soft Delete Example"
    ]

    for user in users + [admin]:
        if not user.is_active:
            continue  # не создаём посты для деактивированных
        for i in range(2):  # 2 поста на пользователя
            post = Posts.objects.create(
                title=random.choice(sample_titles),
                text=f"Пример текста поста {i+1} пользователя {user.username}",
                user=user
            )
            print(f"Создан пост: {post.title} для {user.username}")

# ----------------------------
# Главная функция
# ----------------------------
if __name__ == "__main__":
    admin, users = create_users()
    soft_delete_user(users, username_to_delete="bob")
    create_posts(users, admin)
    print("Тестовые данные успешно созданы!")
