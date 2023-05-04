from setup_db import execute_query
from datetime import datetime
from flask import session



class Messages:
    def __init__(self,message_id:int, message:str, date:int):
        self.message_id=message_id
        self.message=message
        self.date=date
    
    def add(message_str):
        date=datetime.datetime.now()
        date=date.strftime("%x")
        message_to_db=execute_query(
            f"INSERT INTO messages (message , date) VALUES ('{message_str}', '{date}')")

    def show_last5():
        str=execute_query("SELECT message FROM messages")
        messages = []
        for s in str:
            messages.append(s[0])
        last_five=messages[-5:]
        return last_five     



class Student:
    def __init__(self,student_id:int, name:str, email:str, course:str) -> None:
        self.student_id=student_id
        self.name=name
        self.email=email
        self.course=course
    

    def show_info(email):
        info=execute_query(f"SELECT student_id,name FROM students WHERE email='{email}'")
        session["id"]=info[0][0]
        course_name=execute_query(f"""
        SELECT students_courses.course_id , active_courses.name FROM active_courses
        JOIN students_courses
        ON students_courses.student_id={info[0][0]}
        WHERE active_courses.course_id=students_courses.course_id""")
        student=[]
        student.append(Student(name=info[0][1],email=session["username"], course=course_name[0][1]))

        
    def update(email, name):
        execute_query(
        f"""UPDATE students SET email='{email}' WHERE= name='{name}' """)

    

