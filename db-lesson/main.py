import sqlite3
import pandas as pd

connection = sqlite3.connect("baza.db")
cursor = connection.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS job_titles (
    id_job_title INTEGER PRIMARY KEY NOT NULL UNIQUE,
    name TEXT NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    id_job_title INTEGER NOT NULL,
    FOREIGN KEY (id_job_title) REFERENCES job_titles (id_job_title)
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS clients (
    id_client INTEGER PRIMARY KEY NOT NULL UNIQUE,
    organization TEXT NOT NULL,
    phone TEXT NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS orders (
    id_order INTEGER PRIMARY KEY NOT NULL UNIQUE,
    id_client INTEGER NOT NULL,
    id_employee INTEGER NOT NULL,
    amount REAL NOT NULL,
    completion_date TEXT,
    is_completed INTEGER,
    FOREIGN KEY (id_client) REFERENCES clients (id_client),
    FOREIGN KEY (id_employee) REFERENCES employees (id)
);
"""
)

job_titles_data = [
    (1, "Менеджер"),
    (2, "Разработчик"),
    (3, "Аналитик"),
    (4, "Дизайнер"),
    (5, "Тестировщик"),
    (6, "Team Lead"),
]
# with open("name_of_data_file.csv") as file:
#     for row in pd.read_csv(file):
#         cursor.executemany("ISNERT OR IGNORE INTO (job_titles, name) VALUES (?, ?)", row)
cursor.executemany(
    "INSERT OR IGNORE INTO job_titles (id_job_title, name) VALUES (?, ?)",
    job_titles_data,
)

employees_data = [
    (1, "Иванов", "Иван", 2),
    (2, "Петров", "Петр", 1),
    (3, "Сидорова", "Мария", 3),
    (4, "Козлов", "Алексей", 2),
    (5, "Васильева", "Ольга", 4),
    (6, "Соколов", "Дмитрий", 2),
    (7, "Кузнецова", "Анна", 5),
    (8, "Смирнов", "Игорь", 6),
]
cursor.executemany(
    "INSERT OR IGNORE INTO employees (id, surname, name, id_job_title) VALUES (?, ?, ?, ?)",
    employees_data,
)

clients_data = [
    (1, "ТехноПром", "+7-900-111-22-33"),
    (2, "МедиаГрупп", "+7-900-444-55-66"),
    (3, "СтройСервис", "+7-900-777-88-99"),
    (4, "ЭкоЛайн", "+7-900-000-11-22"),
]
cursor.executemany(
    "INSERT OR IGNORE INTO clients (id_client, organization, phone) VALUES (?, ?, ?)",
    clients_data,
)

orders_data = [
    (1, 1, 1, 50000.0, "2023-10-01", 1),
    (2, 2, 4, 120000.0, "2023-10-15", 0),
    (3, 3, 6, 75000.0, "2023-11-01", 1),
    (4, 1, 8, 200000.0, "2023-12-20", 0),
    (5, 4, 2, 15000.0, "2023-09-25", 1),
]
cursor.executemany(
    "INSERT OR IGNORE INTO orders (id_order, id_client, id_employee, amount, completion_date, is_completed) VALUES (?, ?, ?, ?, ?, ?)",
    orders_data,
)

connection.commit()

cursor.execute("SELECT COUNT(*) as total_emloyees FROM employees")
print(f"Всего сотрудников: {cursor.fetchall()[0][0]}")

cursor.execute("SELECT AVG(amount) as average_amount FROM orders")
print(f"Средний чек: {cursor.fetchone()[0]}")

cursor.execute("SELECT SUM(amount) FROM orders WHERE is_completed = 1")
print(f"Сумма выручки по выполненным заказам: {cursor.fetchall()[0][0]}")

cursor.execute("SELECT MAX(amount) as max_amount FROM orders")
print(f"Максимальная стоимость заказа: {cursor.fetchall()[0][0]}")

cursor.execute("SELECT MIN(amount) as min_amount FROM orders")
print(f"Минимальая стоимость заказа: {cursor.fetchall()[0][0]}")


cursor.execute("SELECT is_completed, SUM(amount) FROM orders GROUP BY is_completed")
print(f"Сумма по статусам : {cursor.fetchall()}")

cursor.execute("SELECT id_job_title, COUNT(id) FROM employees GROUP BY id_job_title")
print(f"Кол-во сотрудников по должностям: {cursor.fetchall()}")

cursor.execute("SELECT AVG(amount) FROM orders GROUP BY id_client")
print(f"Средние чеки клиентов: {cursor.fetchall()}")

cursor.execute(
    """SELECT e.name, e.surname, j.name
               FROM employees e
               JOIN job_titles j ON e.id_job_title = j.id_job_title"""
)
print("Сотрудники и должности: ", cursor.fetchall())

cursor.execute(
    """SELECT e.name, e.surname, sum(o.amount)
               FROM employees e
               JOIN orders o ON e.id = o.id_employee
               GROUP BY e.id"""
)
print("Продажи по сотрудникам:", cursor.fetchall())

cursor.execute(
    """
    SELECT DISTINCT c.organization, sum(o.amount)
    FROM clients c
    JOIN orders o ON c.id_client = o.id_client
    WHERE o.is_completed = 0 AND o.amount > 50000
    GROUP BY c.id_client
"""
)
print("Крупные клиенты с активными заказами:", cursor.fetchall())

connection.close()
