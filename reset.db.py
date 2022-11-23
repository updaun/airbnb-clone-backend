import os
import shutil

reset_migrations_list = [
    "users/migrations",
]


def reset_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def reset_migrate(reset_dir):
    for item in os.listdir(reset_dir):
        if item != "__init__.py":
            target_path = os.path.join(reset_dir, item)
            if os.path.isfile(target_path):
                print(f"delete {target_path}")
                os.remove(target_path)


def reset_migrations():
    for reset_dir in reset_migrations_list:
        reset_migrate(reset_dir)


if os.path.isfile("db.sqlite3"):
    os.remove("db.sqlite3")

reset_migrations()

os.system("python manage.py makemigrations")

os.system("python manage.py migrate")
