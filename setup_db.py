import sqlite3
import faker
import random
import datetime

# x = datetime.datetime.now()
# date=x.strftime("%x")





def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur=conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

def create_tables():
    execute_query("""
         CREATE TABLE IF NOT EXISTS messages (
            message TEXT NOT NULL,
            date TEXT NOT NULL
            )
        """)
    
    execute_query("""
    CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL UNIQUE,
            image TEXT DEFAULT 'anonymous.png',
            FOREIGN KEY (user_id) REFERENCES users (user_id)
         )
         """)
    execute_query("""
         CREATE TABLE IF NOT EXISTS active_courses (
            course_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            date TEXT,
            file TEXT,
            FOREIGN KEY (teacher_id) REFERENCES techers (teacher_id)
            )
        """)
    
    execute_query("""
         CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            image TEXT
            )
         """)
    execute_query("""  
         CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            image TEXT DEFAULT 'anonymous.png',
            FOREIGN KEY (user_id) REFERENCES users (user_id)
         )
         """)
    execute_query("""  
         CREATE TABLE IF NOT EXISTS role (
            role_id INTEGER PRIMARY KEY UNIQUE,
            title TEXT NOT NULL
         )
         """)
    execute_query("""  
         CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL ,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES role (role_id)
         )
         """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students_courses (
            id INTEGER PRIMARY KEY,
            student_id INTEGER ,
            course_id INTEGER ,
            grade INTEGER,
            UNIQUE(student_id,course_id),
            FOREIGN KEY (student_id) REFERENCES students (studnet_id),
            FOREIGN KEY (course_id) REFERENCES active_courses (course_id)
         )  
         """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            date TEXT,
            present TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_id) REFERENCES active_courses (course_id),
            UNIQUE(course_id,student_id,date)
         )  
         """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            details TEXT
            
         )  
         """)

    
def create_fake_data(students_num=40 , teacher_num=4):
    fake=faker.Faker()
    i=0
    for student in range(students_num):
        i+=1
        email=fake.email()
        execute_query(f"INSERT INTO students (name, email,user_id) VALUES ('{fake.name()}','{email}',{i})")
        execute_query(f"INSERT INTO users (username, password,role_id) VALUES ('{email}','{email}',1)")
    execute_query(f"INSERT INTO students (name, email,user_id) VALUES ('student','student@test.org',41)")
    execute_query(f"INSERT INTO users (username, password,role_id) VALUES ('student@test.org','student@test.org',1)")
    i+=1
    for teacher in range(teacher_num):
        i+=1
        emailt=fake.email()
        execute_query(f"INSERT INTO teachers (name, email,user_id) VALUES ('{fake.name()}','{emailt}',{i})")
        execute_query(f"INSERT INTO users (username, password,role_id) VALUES ('{emailt}','{emailt}',2)")
    execute_query(f"INSERT INTO teachers (name, email,user_id) VALUES ('teacher','teacher@test.org',5)")
    execute_query(f"INSERT INTO users (username, password,role_id) VALUES ('teacher@test.org','teacher@test.org',2)")
    courses=['python','java','html','css','javascript']
    for course_name in courses:
        teacher_ids=[tup[0] for tup in execute_query("SELECT teacher_id FROM teachers")]
        execute_query(f"INSERT INTO active_courses (name, teacher_id) VALUES ('{course_name}','{random.choice(teacher_ids)}')")
        execute_query(f"INSERT INTO courses (name) VALUES ('{course_name}')")
    for i in range(1,41):
        x=random.randint(1,6)
        execute_query(f"INSERT INTO students_courses (student_id, course_id, grade) VALUES ({i},{x},0)")
        execute_query(f"INSERT INTO attendance (student_id, course_id, date) VALUES ({i},{x},'2023-03-08')")
        
    execute_query("INSERT INTO role (role_id, title) VALUES (1, 'student')")
    execute_query("INSERT INTO role (role_id, title) VALUES (2, 'techer')")
    execute_query("INSERT INTO role (role_id, title) VALUES (3, 'admin')")
    execute_query("INSERT INTO users (username, password,role_id) VALUES ('admin@test.org','admin@test.org', 3)")
    
    execute_query("UPDATE courses SET description='Learn Python including Excel/Database/Test/Network Automation, Data Analysis, Web Development, REST APIs, GraphQL & more' WHERE name='python'")
    execute_query("UPDATE courses SET description='The modern JavaScript course for everyone! Master JavaScript with projects, challenges and theory. Many courses in one!' WHERE name='javascript'")
    execute_query("UPDATE courses SET description='Learn Java In This Course And Become a Computer Programmer. Obtain valuable Core Java Skills And Java Certification' WHERE name='java'")
    execute_query("UPDATE courses SET description='Go From Beginner To HTML Master In A Single Day!' WHERE name='html'")
    execute_query("UPDATE courses SET description='Learn CSS for the first time or brush up your CSS skills and dive in even deeper. EVERY web developer has to know CSS.' WHERE name='css'")

if __name__=="__main__":
    create_tables()
    create_fake_data()
    #the functions will run only when we run setup_db.py