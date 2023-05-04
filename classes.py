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

    
#go over again, parts and details are missing
class Course:
    def __init__(self, course_id:int,course_name:str, date:str, teacher_id:int):
        course_id=course_id
        course_name=course_name
        date=date
        teacher_id=teacher_id
    
    def add(course_name, teacher_id,start_date): 
        execute_query(
            f"INSERT INTO active_courses (name, teacher_id ,date) VALUES ('{course_name}','{teacher_id}','{start_date}')")

    def show_all():
         pass
    def delete():
        pass


class Teacher:
    def __init__(self, teacher_id:int,name:str):
        teacher_id=teacher_id
        name=name

    def show_all():
        pass
    def update():
        pass
    def delete():
        pass

class Attendance:
    def __init__(self,atten_id:int,student_id:int,student_name:str ,course_id:int,course_name:str,date:str,present:str ):
        atten_id=atten_id
        student_id=student_id
        student_name=student_name
        course_id=course_id
        course_name=course_name
        date=date
        present=present

    def show_by_id_date_info(course_id, atten_date):
        info=execute_query(
                f"""SELECT students_courses.course_id, students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
            JOIN attendance on students_courses.student_id=attendance.student_id
            WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}'
            """)
        return info
    
    def show_by_id_date_lst(course_id,atten_date):
        attendance_lst=[]
        info=execute_query(
                f"""SELECT students_courses.course_id, students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
            JOIN attendance on students_courses.student_id=attendance.student_id
            WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}'
            """)
        course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={id}")
        for a_tuple in info:
            attendance_lst.append(Attendance(
                course_id=a_tuple[0],course_name=course_name,student_id=a_tuple[1],student_name=a_tuple[4],date=a_tuple[2],present=a_tuple[3]))
        return attendance_lst
    
    def show_by_student_date(course_id,student_id, atten_date):
        info=execute_query(f"""
        SELECT students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
        JOIN students on students_courses.student_id=students.student_id
        JOIN attendance on students_courses.student_id=attendance.student_id 
        WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}' AND students_courses.student_id={student_id}""")
        return info
    
    def show_by_student_date_lst(course_id,student_id, atten_date):
        result=[]
        info=execute_query(f"""
        SELECT students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
        JOIN students on students_courses.student_id=students.student_id
        JOIN attendance on students_courses.student_id=attendance.student_id 
        WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}' AND students_courses.student_id={student_id}""")

        course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={course_id}")
        for result_tuple in info:
            result.append(Attendance(
                course_id=course_id,course_name=course_name,student_id=result_tuple[0],student_name=result_tuple[1],date=result_tuple[2],present=result_tuple[3]))


    def add(student_id, course_id, atten_date):
        execute_query(f"INSERT INTO attendance (student_id, course_id, date) VALUES ({student_id}, {course_id}, '{atten_date}') ")