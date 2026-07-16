import sqlite3
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE students (
 id INTEGER,
name TEXT,
age INTEGER             
)
""")
cursor.execute("""
INSERT INTO students (id,name,age)
values (1,'rahul',17)

""")
cursor.execute("""
INSERT INTO students(id,name,age)
values (2,'aman',19)
               
  """)

conn.commit()
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()
print(students)
conn.close()
