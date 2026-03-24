import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return cur.fetchall()


# 1. Отримати всі завдання певного користувача (user_id = 1)
sql_1 = """
SELECT t.id, t.title, t.description, s.name AS status, u.fullname
FROM tasks AS t
JOIN status AS s ON t.status_id = s.id
JOIN users AS u ON t.user_id = u.id
WHERE t.user_id = 1;
"""

# 2. Вибрати завдання за статусом 'new' (через підзапит)
sql_2 = """
SELECT t.id, t.title, t.description
FROM tasks AS t
WHERE t.status_id IN (
    SELECT id FROM status WHERE name = 'new'
);
"""

# 3. Оновити статус конкретного завдання (id = 1) на 'in progress'
sql_3 = """
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;
"""

# 4. Отримати список користувачів, які не мають жодного завдання
sql_4 = """
SELECT *
FROM users
WHERE id NOT IN (
    SELECT user_id FROM tasks WHERE user_id IS NOT NULL
);
"""

# 5. Додати нове завдання для конкретного користувача (user_id = 1)
sql_5 = """
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'New feature',
    'Implement dark mode',
    (SELECT id FROM status WHERE name = 'new'),
    1
);
"""

# 6. Отримати всі завдання, які ще не завершено
sql_6 = """
SELECT t.id, t.title, s.name AS status
FROM tasks AS t
JOIN status AS s ON t.status_id = s.id
WHERE s.name != 'completed';
"""

# 7. Видалити конкретне завдання (id = 2)
sql_7 = """
DELETE FROM tasks WHERE id = 2;
"""

# 8. Знайти користувачів з певною електронною поштою (домен @example.com)
sql_8 = """
SELECT * FROM users
WHERE email LIKE '%@example.com';
"""

# 9. Оновити ім'я користувача (id = 1)
sql_9 = """
UPDATE users
SET fullname = 'Updated Name'
WHERE id = 1;
"""

# 10. Отримати кількість завдань для кожного статусу
sql_10 = """
SELECT s.name AS status, COUNT(t.id) AS count
FROM status AS s
LEFT JOIN tasks AS t ON s.id = t.status_id
GROUP BY s.id;
"""

# 11. Завдання користувачів з певним доменом електронної пошти
sql_11 = """
SELECT t.id, t.title, s.name AS status, u.email
FROM tasks AS t
JOIN status AS s ON t.status_id = s.id
JOIN users AS u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';
"""

# 12. Отримати список завдань, що не мають опису
sql_12 = """
SELECT t.id, t.title, s.name AS status
FROM tasks AS t
JOIN status AS s ON t.status_id = s.id
WHERE t.description IS NULL;
"""

# 13. Користувачі та їхні завдання зі статусом 'in progress' (INNER JOIN)
sql_13 = """
SELECT u.fullname, t.title, s.name AS status
FROM users AS u
INNER JOIN tasks AS t ON u.id = t.user_id
INNER JOIN status AS s ON t.status_id = s.id
WHERE s.name = 'in progress';
"""

# 14. Отримати користувачів та кількість їхніх завдань (LEFT JOIN + GROUP BY)
sql_14 = """
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users AS u
LEFT JOIN tasks AS t ON u.id = t.user_id
GROUP BY u.id;
"""


if __name__ == '__main__':
    print("1. Завдання користувача з user_id = 1:")
    print(execute_query(sql_1), "\n")

    print("2. Завдання зі статусом 'new' (підзапит):")
    print(execute_query(sql_2), "\n")

    print("3. Оновлення статусу завдання id=1 на 'in progress':")
    execute_query(sql_3)
    print("Виконано\n")

    print("4. Користувачі без жодного завдання:")
    print(execute_query(sql_4), "\n")

    print("5. Додавання нового завдання для user_id = 1:")
    execute_query(sql_5)
    print("Виконано\n")

    print("6. Незавершені завдання:")
    print(execute_query(sql_6), "\n")

    print("7. Видалення завдання з id = 2:")
    execute_query(sql_7)
    print("Виконано\n")

    print("8. Користувачі з email '@example.com':")
    print(execute_query(sql_8), "\n")

    print("9. Оновлення імені користувача id=1:")
    execute_query(sql_9)
    print("Виконано\n")

    print("10. Кількість завдань за статусами:")
    print(execute_query(sql_10), "\n")

    print("11. Завдання юзерів з доменом '@example.com':")
    print(execute_query(sql_11), "\n")

    print("12. Завдання без опису:")
    print(execute_query(sql_12), "\n")

    print("13. Користувачі та завдання зі статусом 'in progress':")
    print(execute_query(sql_13), "\n")

    print("14. Кількість завдань кожного користувача:")
    print(execute_query(sql_14), "\n")