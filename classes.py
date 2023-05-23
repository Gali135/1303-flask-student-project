from setup_db import execute_query
from datetime import datetime
from flask import session
import statistics
import sqlite3
import json


class Messages:
    def __init__(self,message_id:int, message:str, date:int):
        self.message_id=message_id
        self.message=message
        self.date=date
    
    def add(message_str):
        date=datetime.now()
        date=date.strftime("%x")
        message_to_db=execute_query(
            f"INSERT INTO messages (message , date) VALUES ('{message_str}', '{date}')")

    def show_last5():
        str=execute_query("SELECT message,date FROM messages")
        messages = []
        for s in str:
            messages.append([s[0],s[1]])
        last_five=messages[-5:]
        return last_five     



class Student:
    def __init__(self,student_id:int, name:str, email:str,courses, img:None) -> None:
        self.student_id=student_id
        self.name=name
        self.email=email
        self.courses=courses
        self.img=img
       

    def show_info(email):
        info=execute_query(f"SELECT student_id,name,image FROM students WHERE email='{email}'")
        student=[]
        student.append(Student(student_id=session["id"],name=info[0][1], email=session["username"],courses=[],img=info[0][2]))
        return student
    
    def show_all():
        students=[]
        course_lst=[]
        
        
        student_info=execute_query(f"""SELECT students.student_id, students.name, students.email,image FROM students""")
        for tuple in student_info:
            course_lst=[]
            course=execute_query(f"""
                SELECT active_courses.name ,students_courses.grade, students_courses.course_id
                FROM students_courses 
                JOIN active_courses ON active_courses.course_id = students_courses.course_id
                WHERE students_courses.student_id={tuple[0]};
            """)
            for course_tuple in course:
                #course(name, grade, course_id)
                course_lst.append([course_tuple[0],course_tuple[1],course_tuple[2]])
                
    
            students.append(Student(
                student_id=tuple[0], name=tuple[1],email=tuple[2],courses=course_lst,img=tuple[3]))
        return students

    def show_all_search(name):
        students=[]
        course_lst=[]
        
        
        result=execute_query(f"""
            SELECT student_id, name , email FROM students WHERE students.name  LIKE '{name}%' 
            UNION
            SELECT student_id, name , email FROM students WHERE students.email  LIKE '{name}%' """)
        for tuple in result:
            course_lst=[]
            course=execute_query(f"""
                SELECT active_courses.name ,students_courses.grade, students_courses.course_id
                FROM students_courses 
                JOIN active_courses ON active_courses.course_id = students_courses.course_id
                WHERE students_courses.student_id={tuple[0]};
            """)
            for course_tuple in course:
                #course(name, grade, course_id)
                course_lst.append([course_tuple[0],course_tuple[1],course_tuple[2]])
                
    
            students.append(Student(
                student_id=tuple[0], name=tuple[1],email=tuple[2],courses=course_lst))
        return students



    def update(n_email, o_email):
        execute_query(f"""
            UPDATE students SET email='{n_email}' WHERE email='{o_email}' """)
        execute_query(f"""
            UPDATE users SET username='{n_email}', password='{n_email} WHERE username='{o_email}' """)

    def json_result():
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name,email FROM students")
        info = cursor.fetchall()
        conn.close()

        # Convert the query results to JSON
        json_results = []
        for row in info:
            row_dict = dict(zip([column[0] for column in cursor.description], row))
            json_results.append(row_dict)

        return json_results


    
#go over again, parts and details are missing
class PublicCourse:
    def __init__(self,id: int,name :str, description:str, image:str):
        self.id=id
        self.name=name
        self.description=description
        self.image=image

    def show_info():
        lst=[]
        info=execute_query(f"SELECT * FROM courses")
        for tuple in info:
            lst.append(PublicCourse(id=tuple[0],name=tuple[1], description=tuple[2],image=tuple[3]))
        return lst


    def add(name, description,image): 
        execute_query(
            f"INSERT INTO courses (name, description ,image) VALUES ('{name}','{description}','{image}')")

    def update(name, change):
        pass
    def delete(name):
        pass

class Course:
    def __init__(self, course_id:int,course_name:str, date:str, teacher_id:int,file:None):
        self.course_id=course_id
        self.course_name=course_name
        self.date=date
        self.teacher_id=teacher_id
        self.file=file
    
    def add(course_name, teacher_id,start_date,file): 
        execute_query(
            f"INSERT INTO active_courses (name, teacher_id ,date,file) VALUES ('{course_name}','{teacher_id}','{start_date}','{file}')")

    def show_all():
         pass
    def update(course_id, file, start_date):
        print(f"file={file} course_id={course_id} date{start_date}")
        if file=="" and start_date != "":
            a=execute_query(f"UPDATE active_courses SET date='{start_date}' WHERE course_id={course_id}")
            return
        elif file !="" and start_date =="":
             b=execute_query(f"UPDATE active_courses SET file='{file}' WHERE course_id={course_id}")
             return
        c=execute_query=(f"""
            UPDATE active_courses SET file='{file}' ,date='{start_date}' WHERE course_id={course_id}""")
        return
    
    def delete():
        pass


class Teacher:
    def __init__(self, teacher_id:int,name:str, email:str, courses:str,img:None):
        self.teacher_id=teacher_id
        self.name=name
        self.email=email
        self.courses=courses
        self.img=img
        
    # def show_info(id):
    #     info=[]
    #     teacher=execute_query(f"SELECT * FROM teachers WHERE teacher_id={id}")
        
    def show_all():
        
        teachers=[]
        teacher=execute_query(f"""SELECT teachers.teacher_id, teachers.name, teachers.email,image FROM teachers""")
        for teacher_tuple in teacher:
            course_lst=[]
            course=execute_query(f"""
                SELECT name, course_id FROM active_courses 
                WHERE teacher_id={teacher_tuple[0]}""")
            for course_tuple in course:
                # course_lst(name, course_id)
                course_lst.append([course_tuple[0],course_tuple[1]])

            teachers.append(Teacher(teacher_id=teacher_tuple[0], name=teacher_tuple[1],email=teacher_tuple[2],courses=course_lst,img=teacher_tuple[3]))
        return teachers


    def show_all_search(name):
        teachers=[]
        result=execute_query(f"""
            SELECT teacher_id, name , email FROM teachers WHERE teachers.name  LIKE '{name}%' 
            UNION
            SELECT teacher_id, name , email FROM teachers WHERE teachers.email  LIKE '{name}%' """)
        
        for teacher_tuple in result:
            course_lst=[]
            course=execute_query(f"""
                SELECT name, course_id FROM active_courses 
                WHERE teacher_id={teacher_tuple[0]}""")
            for course_tuple in course:
                # course_lst(name, course_id)
                course_lst.append([course_tuple[0],course_tuple[1]])

            teachers.append(Teacher(teacher_id=teacher_tuple[0], name=teacher_tuple[1],email=teacher_tuple[2],courses=course_lst))
        return teachers

    def update(n_email, o_email):
        execute_query(
        f"""UPDATE teachers SET email='{n_email}' WHERE email='{o_email}' """)
        execute_query(
        f"""UPDATE users SET username='{n_email}', password='{n_email}' WHERE username='{o_email}' """)

    def delete():
        pass
    
    def avg(course_id):
        avg="No Data Available"
        grades_lst=[]
        grades=execute_query(f"""
            SELECT grade FROM students_courses
            WHERE course_id={course_id}""")
        for tuple in grades:
            if tuple[0] != None:
                grades_lst.append(tuple[0])
        if len(grades_lst)>0:
            avg=round(statistics.mean(grades_lst),2)
        return avg  
   


class Attendance:
    def __init__(self,student_id:int,student_name:str ,course_id:int,course_name:str,date:str,present:str ):
        self.student_id=student_id
        self.student_name=student_name
        self.course_id=course_id
        self.course_name=course_name
        self.date=date
        self.present=present

    def show_by_id_date_info(course_id, atten_date):
        info=execute_query(f"""
            SELECT students_courses.course_id, students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
            JOIN attendance on students_courses.student_id=attendance.student_id
            WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}'
            """)
        return info
    
    def show_by_id_date_lst(course_id,atten_date):
        attendance_lst=[]
        info1=execute_query(f"""
            SELECT students_courses.course_id, students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
            JOIN attendance on students_courses.student_id=attendance.student_id
            WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}'
            """)
       
        course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={course_id}")[0]
        for a_tuple in info1:
            attendance_lst.append(Attendance(
                course_id=a_tuple[0],course_name=course_name,student_id=a_tuple[1],student_name=a_tuple[2],date=a_tuple[3],present=a_tuple[4]))
        return attendance_lst

    def show_by_student_date(course_id,student_id, atten_date):
        #returning raw data
        info=execute_query(f"""
            SELECT students_courses.student_id , students.name , attendance.date, attendance.present FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
            JOIN attendance on students_courses.student_id=attendance.student_id 
            WHERE students_courses.course_id={course_id} AND attendance.date='{atten_date}' AND students_courses.student_id={student_id}""")
        return info
    
    def show_by_student_date_lst(course_id,student_id, atten_date):
        #returning list of objects
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
        return result
    
    def add(student_id, course_id, atten_date):
        execute_query(f"INSERT INTO attendance (student_id, course_id, date) VALUES ({student_id}, {course_id}, '{atten_date}') ")

