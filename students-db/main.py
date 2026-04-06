import sqlite3

conn = sqlite3.connect("students_db.db")
cursor = conn.cursor()

qwery = """
    CREATE TABLE IF NOT EXISTS level_of_education (
        id_level INTEGER PRIMARY KEY,
        name VARCHAR
    );
"""
cursor.execute(qwery)
qwery = """
    CREATE TABLE IF NOT EXISTS specialty (
        id_specialty INTEGER PRIMARY KEY,
        name VARCHAR
    );
"""
cursor.execute(qwery)
qwery = """
    CREATE TABLE IF NOT EXISTS type_of_education (
        id_type INTEGER PRIMARY KEY,
        name VARCHAR
    );
"""
cursor.execute(qwery)
qwery = """
    CREATE TABLE IF NOT EXISTS students (
        id_student INTEGER PRIMARY KEY,
        id_level INTEGER,
        id_specialty INTEGER,
        id_type INTEGER,
        surname VARCHAR,
        name VARCHAR,
        fathername VARCHAR,
        average_mark INTEGER,
        
        FOREIGN KEY (id_level) REFERENCES level_of_education(id_level),
        FOREIGN KEY (id_specialty) REFERENCES specialty(id_specialty),
        FOREIGN KEY (id_type) REFERENCES type_of_education(id_type)
    );
"""
cursor.execute(qwery)

with open("table_data/level_of_education.txt") as file:
    levels = [line.strip().split() for line in file]
    
cursor.executemany("INSERT OR IGNORE INTO level_of_education VALUES (?, ?)", levels)

with open("table_data/types_of_education.txt") as file:
    types = [line.strip().split() for line in file]
    
cursor.executemany("INSERT OR IGNORE INTO type_of_education VALUES (?, ?)", types)

with open("table_data/specialties.txt") as file:
    specialties = [line.strip().split() for line in file]
        
cursor.executemany("INSERT OR IGNORE INTO specialty VALUES (?, ?)", specialties)

with open("table_data/students.txt") as file:
    students = [line.strip().split() for line in file]
        
cursor.executemany("INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)", students)

conn.commit()

cursor.execute("""
               SELECT COUNT(*)
               FROM students;
               """)
print("Всего студентов: ", cursor.fetchone()[0])

cursor.execute("""
               SELECT s.name, COUNT(st.id_student)
               FROM specialty s
               JOIN students st ON s.id_specialty = st.id_specialty
               GROUP BY s.name;
               """)
print("Всего студентов по направлениям: ", cursor.fetchall())

cursor.execute("""
               SELECT t.name, COUNT(st.id_student)
               FROM type_of_education t
               JOIN students st ON t.id_type = st.id_type
               GROUP BY t.name;
               """)
print("Всего студентов по типу обучения: ", cursor.fetchall())

cursor.execute("""
               SELECT t.name, MAX(st.average_mark), MIN(st.average_mark), AVG(st.average_mark)
               FROM type_of_education t
               JOIN students st ON t.id_type = st.id_type
               GROUP BY t.name;
               """)
print("Максимальный, минимальный, средний баллы студентов по направлениям: ", cursor.fetchall())

cursor.execute("""
               SELECT s.name, l.name, t.name, AVG(st.average_mark)
               FROM students st
               JOIN specialty s ON s.id_specialty = st.id_specialty
               JOIN level_of_education l ON l.id_level = st.id_level
               JOIN type_of_education t ON t.id_type = st.id_type
               GROUP BY s.name, l.name, t.name;
               """)
print("Средний балл студентов по направления, уровням и формам обучения: ", cursor.fetchall())


cursor.execute("""
    SELECT st.surname, st.name, st.average_mark
    FROM students st
    JOIN specialty s ON st.id_specialty = s.id_specialty
    JOIN type_of_education t ON st.id_type = t.id_type
    WHERE s.name = 'Прикладная_Информатика' AND t.name = 'очная'
    ORDER BY st.average_mark DESC
    LIMIT 5;
""")
print("Кандидаты на повышенную стипендию:", cursor.fetchall())


cursor.execute("""
    SELECT surname, COUNT(*)
    FROM students
    GROUP BY surname
    HAVING COUNT(*) > 1;
""")
print("Однофамильцы:", cursor.fetchall())

cursor.execute("""
    SELECT surname, name, fathername, COUNT(*)
    FROM students
    GROUP BY surname, name, fathername
    HAVING COUNT(*) > 1;
""")
print("Полные тезки:", cursor.fetchall())
