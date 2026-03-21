from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_TASKS= 10
NUMBER_USERS = 30
STATUSES = [('new',), ('in progress',), ('completed',)]

def generate_fake_data(number_tasks, number_users) -> tuple():
    fake_tasks = []# тут зберігатимемо завдання
    fake_users = []# тут зберігатимемо студентів (користувачів)
    '''Візьмемо три завдання з faker і помістимо їх у потрібну змінну'''
    fake_data = faker.Faker()

# Створимо набір компаній у кількості number_tasks
    for _ in range(number_tasks):
        fake_tasks.append((
            fake_data.sentence(nb_words=4),
            fake_data.text(max_nb_chars=200),
        ))

# Згенеруємо тепер number_users кількість студентів'''
    for _ in range(number_users):
        fake_users.append((
            fake_data.name(),
            fake_data.unique.email(),
        ))

    return fake_tasks, fake_users

def insert_data(tasks, users):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()

    # Статуси
    cur.executemany("INSERT OR IGNORE INTO status (name) VALUES (?)", STATUSES)

    # Отримуємо id зі збережених записів
    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    cur.executemany(
        'INSERT INTO users (fullname, email) VALUES (?, ?)', users
    )

    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    # Завдання
    tasks_with_ids = [
        (title, desc, choice(status_ids), choice(user_ids))
        for title, desc in tasks
    ]
    cur.executemany(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
        tasks_with_ids
    )

    conn.commit()
    conn.close()
    print("Дані додано до бази.")

if __name__ == '__main__':
    tasks, users = generate_fake_data(NUMBER_TASKS, NUMBER_USERS)
    insert_data(tasks, users)
