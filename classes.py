from setup_db import execute_query
from datetime import datetime

class Student:
    def __init__(self,student_id:int, name:str, email:str, course:str) -> None:
        self.student_id=student_id
        self.name=name
        self.email=email
        self.course=course

    def update(email, name):
        execute_query(
        f"""UPDATE students SET email='{email}' WHERE= name='{name}' """)

    

