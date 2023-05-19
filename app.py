from flask import Flask, redirect, url_for, render_template, request, session,abort
from classes import Messages, Student, Course,Attendance,Teacher
from setup_db import execute_query
from collections import namedtuple
import json
import datetime

x = datetime.datetime.now()
date=x.strftime("%x")

id=False
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
def db_messages():
    messages=["Hello! welcome to home page"]
    messages+= execute_query(f"SELECT message, date FROM messages")
   
    print(messages)
    return messages

messages=db_messages()

@app.route('/', methods=['GET', 'POST'])
def home():
    results={}
    #taking down tenporarly render_template("index.html", results=results)
    session["prev_messages"]=len(messages)
    return render_template("index.html")

def authenticate(username,password):
    role= execute_query(f"SELECT role_id FROM users WHERE username='{username}' AND password='{password}'")
    if role==[]:
        return None
    else:
        return role[0][0]


@app.route('/login', methods=['GET', 'POST'])
def login():
    username=execute_query("SELECT username FROM users WHERE user_id=1")[0][0]
    print(f"email={username}")
    if request.method=='POST':
        
        role=authenticate(username, username)
        if role==None:
            return abort(403)
        else:
            session["role"]=role
            session["username"]=username

    
        return redirect(url_for('home'))
    msg= '''
        <form action="/login" method="post">
            <p>Enter username<input type=text name=username>
            <p>Enter Password<input type=text name=password>
            <p><button type="submit">Login</button>
        </form>'''
    return render_template("login.html", msg=msg)

@app.route('/admin/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method=="GET":
        students=[]
        courses=[]
        s=execute_query("SELECT student_id, name FROM students ORDER BY name ASC")
        for tuple in s:
            si=namedtuple("Students", ['s_id','s_name'])
            si.s_id=tuple[0]
            si.s_name=tuple[1]
            students.append(si)
        c=execute_query("SELECT course_id, name, date  FROM active_courses ORDER BY name ASC")
        for tuple in c:
            ci=namedtuple("Courses", ['c_id','c_name', 'date'])
            ci.c_id=tuple[0]
            ci.c_name=tuple[1]
            ci.date=tuple[2]
            courses.append(ci)
        return render_template("register_student.html", students_lst=students, courses_lst=courses)
    else:
        student_id=request.form["students"]
        course_id=request.form["courses"]
        redirect(url_for(f"register({student_id},{course_id})"))
        return



@app.route('/register', methods=['GET', 'POST'])
def register():
    student_id=request.args.get("students")
    course_id=request.args.get("courses")
    # if session.get("role","anonymous")=='admin':
    #     return 'To see this page please log in'
    execute_query(
        f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}','{course_id}')")
    return redirect(url_for('home'))


#messages
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        message_str=request.form["message"]
        Messages.add(message_str=message_str)
    return render_template("admin.html")

@app.route('/messages')
def get_message():
    session["prev_messages"]=len(messages)
    # messages=Messages.show_last5
    return messages[-5:]

@app.route('/num')
def method_name1():
    return str(len(messages))

@app.route('/new_message_counter')
def counter():
    session["new_messages"]=len(messages)-session["prev_messages"]
    return str(session["new_messages"])

@app.route('/add_m', methods=['POST'])
def add():
    Messages.add(request.json["message"])
    return "message added"

@app.route('/add_m')
def add2():
    Messages.add(request.json["message"])
    return "message added"

#student   
@app.route('/student_info', methods=['GET', 'POST']) 
def student_info():
    # if  session["role"] != 1  :
    #     #if  session["role"] not in [1,3]
    #     return abort(403)
    email=session["username"]
    id=execute_query(f"SELECT student_id FROM students WHERE email='{email}'")[0][0]
    session["id"]=id
    student=Student.show_info(email)
    
    course_info=[]
    ci=execute_query(f"""
        SELECT students_courses.course_id ,students_courses.grade, active_courses.name FROM active_courses
        JOIN students_courses
        ON students_courses.student_id={session["id"]}
        WHERE active_courses.course_id=students_courses.course_id""")
    for c in ci:
        course=namedtuple("Courses", ['c_id', 'grade', 'c_name'])
        course.c_id=c[0]
        course.grade=c[1]
        course.c_name=c[2]
        course_info.append(course)
        
        
    return render_template("student_info.html", students=student, course_info=course_info)

@app.route('/student/update', methods=['GET', 'POST'])
def student_update():
    if request.method=="GET":
        email=session["username"]
        name=execute_query(f"SELECT name FROM students WHERE email='{email}'")[0][0]
        return render_template ("student_update.html" ,email=email, s_name=name)
    else:
        n_email=request.form["email"]
        o_email=session["username"]
        Student.update(n_email=n_email,o_email=o_email)
        session.clear()
        session["username"]="n_email"
        return redirect(url_for("student_info"))

#course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    # if session['role']!= 3:
    #         return abort(403)
    teachers = execute_query("SELECT teacher_id , name FROM teachers")
    courses = execute_query("""
    SELECT active_courses.course_id ,active_courses.name ,active_courses.date ,teachers.name 
    FROM active_courses 
    left JOIN teachers 
    on active_courses.teacher_id=teachers.teacher_id
    ORDER BY active_courses.name ASC """)
    teachers_lst = []
    courses_lst = []
    # what SQL Syntax do i need to use to get courses.name and teachers. name when i only have courses_teachers_id
    for teacher_tuple in teachers:
        teacher = namedtuple("Teacher", ['id', 'name'])
        teacher.id = teacher_tuple[0]
        teacher.name = teacher_tuple[1]
        teachers_lst.append(teacher)

    for course_tuple in courses:
        course = namedtuple("Course", ['id','c_name', 't_name','date'])
        course.id = course_tuple[0]
        course.c_name = course_tuple[1]
        course.date=course_tuple[2]
        course.t_name = course_tuple[3]
        courses_lst.append(course)

    if request.method == 'GET':
        return render_template("add_course.html", teachers_lst=teachers_lst, courses_lst=courses_lst)
    else:
        teacher_id = request.form["teacher_id"]
        course_name = request.form["course_name"]
        start_date=request.form["start_date"]
        if start_date == "":
            msg = "Please choose start date for this course and try again"
            return render_template("add_course.html", teachers_lst=teachers_lst, msg=msg)
        if teacher_id == "":
            msg = "Please choose teacher for this course and try again"
            return render_template("add_course.html", teachers_lst=teachers_lst, msg=msg)
        elif course_name == "":
            msg = "Please enter course name and try again"
            return render_template("add_course.html", teachers_lst=teachers_lst, msg=msg)
        else:
            #teacher_id=execute_query(f"SELECT teachers_id FROM teachers WHERE name={teacher_name}")

            try:
                Course.add(course_name, teacher_id,start_date)
            except:
                msg="something went wrong, please try again."
            else:
                msg = "The Course Was Added Successfully !"
                
            return redirect(url_for("add_course"))


@app.route('/courses/students/<id>', methods=['GET','POST'])
def student_courses(id):
    students_course=[]
    info=execute_query(f"""
    SELECT students_courses.course_id, students_courses.student_id ,students_courses.grade, students.name FROM students_courses
    JOIN students on students_courses.student_id=students.student_id
    WHERE students_courses.course_id={id}""")
    course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={id}")[0][0]
    for sc_tuple in info:
        sc=namedtuple("Student_course", ['c_id','c_name','s_id', 's_name','grade'])
        sc.c_id=sc_tuple[0]
        sc.c_name=course_name
        sc.s_id=sc_tuple[1]
        sc.grade=sc_tuple[2]
        sc.s_name=sc_tuple[3]
        students_course.append(sc)
    return render_template("course.html", students_course=students_course)

@app.route('/courses/attendance', methods=['GET', 'POST'])
def courses_attendance():
    # if session['role']!= 3 or 2:
    #         return abort(403)
    teachers = execute_query("SELECT teacher_id , name FROM teachers")
    courses = execute_query("""
    SELECT active_courses.course_id ,active_courses.name ,teachers.name 
    FROM active_courses 
    left JOIN teachers 
    on active_courses.teacher_id=teachers.teacher_id
    ORDER BY active_courses.name ASC """)
    teachers_lst = []
    courses_lst = []
    # what SQL Syntax do i need to use to get courses.name and teachers. name when i only have courses_teachers_id
    for teacher_tuple in teachers:
        teacher = namedtuple("Teacher", ['id', 'name'])
        teacher.id = teacher_tuple[0]
        teacher.name = teacher_tuple[1]
        teachers_lst.append(teacher)

    for course_tuple in courses:
        course = namedtuple("Course", ['id','c_name', 't_name'])
        course.id = course_tuple[0]
        course.c_name = course_tuple[1]
        course.t_name = course_tuple[2]
        courses_lst.append(course)

    if request.method == 'GET':
        return render_template("attendance.html", teachers_lst=teachers_lst, courses_lst=courses_lst)




@app.route('/attendance/<id>', methods=['GET','POST'])
def atten_date(id):
    id=id
    if request.method== "GET":
        return render_template("students_attendance.html" ,id=id)
    else:
        id=request.form['course_id']
        atten_date=request.form['date']
        return redirect(f"/attendance/{id}/{atten_date}")

@app.route('/attendance/<id>/<atten_date>', methods=['GET', 'POST'])
def attendance(id,atten_date):
    if request.method=='GET':
        try:
            info=Attendance.show_by_id_date(id=id, atten_date=atten_date)
            if info==[]:
                raise ValueError
        except:
            student_info=execute_query(f"SELECT student_id FROM students_courses WHERE course_id={id}")
            for student in student_info:
                Attendance.add(student_id=student[0], course_id=id, atten_date=atten_date)
                
        attendance_lst=Attendance.show_by_id_date_lst(id=id, atten_date=atten_date)
        return render_template("students_attendance.html", attendance_lst=attendance_lst ,atten_date=atten_date,id=id)
    
    else:
        id=id
        atten_date=request.form['date']
        return redirect(f"/attendance/{id}/{atten_date}")
    
@app.route('/set', methods=['GET', 'POST'])
def set():
    if request.method=="POST":
        course_id =request.form["course_id"]
        date =request.form["date"]
        student_id =request.form["student_id"]
        present = request.form['my_radio']

        set_i=execute_query(f"""
        UPDATE attendance
        SET present = '{present}'
        WHERE course_id ={course_id} AND student_id={student_id} AND date='{date}'""")

    return redirect(url_for("attendance" ,atten_date=date, id=course_id ))

@app.route('/name_attendance/<id>', methods=['GET', 'POST'])
def name_attendance(id):

    if request.method=='GET':
        
        students_lst=[]
        info=execute_query(f"""
        SELECT students_courses.course_id, students_courses.student_id ,students_courses.grade, students.name FROM students_courses
        JOIN students on students_courses.student_id=students.student_id
        WHERE students_courses.course_id={id}""")
        course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={id}")[0][0]
        for s_tuple in info:
            s=namedtuple("Student", ['c_id','c_name','s_id', 's_name','grade'])
            s.c_id=s_tuple[0]
            s.c_name=course_name
            s.s_id=s_tuple[1]
            s.grade=s_tuple[2]
            s.s_name=s_tuple[3]
            students_lst.append(s)
        return render_template("name_attendance.html", students_lst=students_lst)
       
    else:    
        id=id
        student_id=request.form["name"]
        atten_date=request.form["date"]

        info=execute_query(f"""
        SELECT students_courses.course_id, students_courses.student_id ,students_courses.grade, students.name FROM students_courses
        JOIN students on students_courses.student_id=students.student_id
        WHERE students_courses.course_id={id}""")
        course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={id}")[0][0]
        for s_tuple in info:
            s=namedtuple("Student", ['c_id','c_name','s_id', 's_name','grade'])
            s.c_id=s_tuple[0]
            s.c_name=course_name
            s.s_id=s_tuple[1]
            s.grade=s_tuple[2]
            s.s_name=s_tuple[3]
            students_lst.append(s)

        r_info=r_info=Attendance.show_by_student_date(course_id=id, student_id=student_id, atten_date=atten_date)
            
        if r_info==[]:
            msg="No such records, pleas try a different date "
            return render_template("name_attendance.html", students_lst=students_lst ,results=results,atten_date=atten_date, msg=msg)
            
        results=Attendance.show_by_student_date_lst(course_id=id, student_id=student_id, atten_date=atten_date)

        return render_template("name_attendance.html", students_lst=students_lst ,results=results,atten_date=atten_date)

    
       
            
      
    
      

@app.route('/courses', methods=['GET', 'POST'])
def show_courses():
    courses=[]
    course=execute_query(f"SELECT courses.name , courses.description FROM courses")
    for course_tuple in course:
        course = namedtuple("Course", ['course_name', 'desc'])
        course.course_name = course_tuple[0]
        course.desc = course_tuple[1]
        courses.append(course)
    return render_template("show_courses.html",  courses=courses)


@app.route('/delete_course/<course_id>')
def delete_course(course_id):
    delete=execute_query(f"DELETE FROM active_courses WHERE course_id={course_id}")
    return redirect(url_for("add_course"))
#how do i get the course_id?
    

@app.route('/course/<id>')
def course(id):
    name = execute_query(f"SELECT name FROM active_courses WHERE id={id}")
    return json.dumps(name)
    # the oopsite of dumps is loads


@app.route('/search', methods=['POST'])
def search():
    db_lst=["course","student","teacher"]
    word=request.form["word"]
    results={"course":[],"student":[],"teacher":[]}
    for table in db_lst:
        first=execute_query(f"SELECT name,{table}_id FROM {table}s WHERE name LIKE '{word}%' ")
        if first !="":
            for i in first:
                results[f"{table}"].append({"name":f"{i[0]}", "id":f"{i[1]}"})
                # result[f"{table}"]["id"].append(first[1])
    
    return render_template("index.html" , results=results)
# f __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/')
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'

# 
#     '''
@app.route('/admin/teachers', methods=['GET', 'POST'])
def all_teachers():
    teachers=Teacher.show_all()
    print("this is the lst=")
    print(Teacher.show_all())
    return render_template("show_teachers.html", teachers=teachers)


@app.route('/admin/students', methods=['GET', 'POST'])
def all_students():
    students=Student.show_all()
    return render_template("show_students.html", students=students)


# @app.route('/teacher/<teacher_id>', methods=['POST'])
# def teacher(teacher_id):
#     courses=execute_query(f"SELECT active_course.name, active_courses.course_id FROM active_corses WHERE teacher_id={teacher_id}")
#     info=[]
#     for t_tuple in courses:
#             s=namedtuple("TeacherC", ['c_id','c_name'])
#             s.c_name=t_tuple[0]
#             s.c_id=t_tuple[1]
#             info.append(s)
#     return render_template("#.html" info=info)

@app.route('/teacher/<techer_id>/<course_id>', methods=['POST'])
def method_name():
    pass
    
            
    # for i in range(len(courses)):
    #     info[f"{course[0][i]}"]={"students":[f"""
    #     SELECT students_courses.student_id,students.name, students_corses.grade FROM students
    #     LEFT JOIN students_courses 
    #     ON students_courses.student_id
    #     WHERE students_courses.course_id={course[1][i]}"""]}
    #     #makes no sense!

    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
