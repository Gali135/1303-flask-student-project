from flask import Flask, redirect, url_for, render_template, request, session,abort,jsonify
from classes import Messages, Student, Course,Attendance,Teacher, PublicCourse
from setup_db import execute_query
from collections import namedtuple
import os
import json
import datetime
import statistics

x = datetime.datetime.now()
date=x.strftime("%x")

id=False
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
def db_messages():
    messages=["Hello! welcome to home page"]
    messages+= execute_query(f"SELECT message, date FROM messages")
    return messages

messages=db_messages()

@app.route('/', methods=['GET', 'POST'])
def home():
    results={}
    #taking down tenporarly render_template("index.html", results=results)
    session["prev_messages"]=len(messages)
    return render_template("index.html")

@app.route('/home', methods=['GET', 'POST'])
def anony_home():
    results={}
    #taking down tenporarly render_template("index.html", results=results)
    return render_template("index_anony.html")


@app.route('/add_lead', methods=['GET', 'POST'])
def add_leads():
    name=request.form["name"]
    email=request.form["email"]
    phone=request.form["phone"]
    details=request.form["details"]
    l=execute_query(f"""
        INSERT INTO leads (name, phone ,email, details) 
        VALUES ('{name}','{phone}','{email}','{details}')""")
    return redirect(url_for("anony_home"))


def authenticate(username,password):
    try:
        role= execute_query(f"SELECT role_id FROM users WHERE username='{username}' AND password='{password}'")
    except:
        return None
    if role==[]:
        return None
    return role[0][0]


@app.route('/login', methods=['GET', 'POST'])
def login():
    # username=execute_query("SELECT username FROM users WHERE role_id=2")[0][0]
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]

        x=authenticate(username, password)
        if x==None:
            return abort(403)
        else:
            session["role"]=x
            session["username"]=username

    
        return redirect(url_for('home'))
    msg= '''
        <form action="/login" method="post">
            <br>Enter username<input type="text" name="username">
            <br>Enter Password<input type="password" name="password">
            <br><button type="submit">Login</button>
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
            ci=namedtuple("Courses", ['c_id','c_name', 'date','avg'])
            ci.c_id=tuple[0]
            ci.c_name=tuple[1]
            ci.date=tuple[2]
            ci.avg=Teacher.avg(tuple[0])
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
    return redirect(url_for('admin'))


#messages
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        message_str=request.form["message"]
        Messages.add(message_str=message_str)
    return render_template("admin.html")

@app.route('/messages')
def get_message():
    # session["prev_messages"]=len(messages)
    messages=Messages.show_last5()
    return messages

# @app.route('/num')
# def method_name1():
#     return str(len(messages))

# @app.route('/new_message_counter')
# def counter():
#     session["new_messages"]=len(messages)-session["prev_messages"]
#     return str(session["new_messages"])

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
    if  session["role"] == 2  :
        redirect(url_for("teacher_info"))
    elif session["role"]==3:
        redirect(url_for("admin"))
    else:
        email=session["username"]
        id=execute_query(f"SELECT student_id FROM students WHERE email='{email}'")[0][0]
        print(f"id= {id}")
        session["id"]=id
        student=Student.show_info(email)
        
        course_info=[]
        ci=execute_query(f"""
            SELECT students_courses.course_id ,students_courses.grade, active_courses.name FROM active_courses
            JOIN students_courses
            ON students_courses.student_id={session["id"]}
            WHERE active_courses.course_id=students_courses.course_id""")
        
        if ci== []:
            course=namedtuple("Courses", ['c_id', 'grade', 'c_name'])
            course.c_id="No Date"
            course.grade="No Date"
            course.c_name="No Date"
            course_info.append(course)
        else:
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

@app.route('/student/upload', methods=['GET', 'POST'])
def student_upload():
    if request.method == 'POST':
        file = request.files['img']
        name=request.form["name"]
        if file:
            filename = file.filename
            file.save(os.path.join('static/img/students', filename))
            execute_query(f"UPDATE students SET image ='{filename}' WHERE name ='{name}'")
            return redirect(url_for("student_info"))
    

@app.route('/student_course/<student_id>/<course_id>', methods=['GET', 'POST'])
def student_course(student_id,course_id):
        student_info=[]
        course_info=[]
        a=execute_query(f"SELECT students_courses.grade FROM students_courses WHERE course_id={course_id} AND student_id={student_id}")
        b=execute_query(f"SELECT students.name AS student_name FROM students WHERE student_id={student_id}")
        c=execute_query(f"""
            SELECT active_courses.name AS course_name, active_courses.teacher_id, teachers.name AS teacher_name,teachers.email 
            FROM active_courses
            JOIN teachers ON active_courses.teacher_id=teachers.teacher_id WHERE active_courses.course_id={course_id}
            """)

        for tuple in c:
            course=namedtuple("Course", ['course_id','course_name','teacher_name', 'email'])
            course.course_id=course_id
            course.course_name=tuple[0]
            course.teacher_name=tuple[2]
            course.email=tuple[3]
            course_info.append(course)
        
        student=namedtuple("Student",['grade','per_presence','student_name'])
        student.grade=a[0][0]
        student.student_name=b[0][0]  
        student.per_presence=per_presence_by_id_course(student_id, course_id)
        student_info.append(student)
        return render_template("student_course.html", course_info=course_info, student_info=student_info)



#teachers
def per_presence_by_id_course(student_id, course_id):
    i=0
    percentage="No Data Available"
    info=execute_query(f"""
        SELECT present FROM attendance 
        WHERE student_id={student_id} AND course_id={course_id}""")
    dates_num=len(info)
    for tuple in info:
            if tuple[0]=="y":
                i+=1
    if i!=0:
        percentage=(i / dates_num)*100   
    return percentage

def per_presence_course(course_id):
    presence=0
    percentage="No Data Available"
    date=execute_query(f"""SELECT date FROM attendance WHERE course_id={course_id}""")
    dates_num=len(date)
    for date_tuple in date:
        info=execute_query(f"""
        SELECT present FROM attendance 
        WHERE course_id={course_id} AND date='{date_tuple[0]}'""")
        students_num=len(info)
        for tuple in info:
                if tuple[0]=="y":
                    presence+=1
        
    if presence !=0:
        percentage=(presence/(students_num * dates_num)) * 100
    
     
    return percentage

 
@app.route('/teacher_info', methods=['GET', 'POST']) 
def teacher_info():

    if  session["role"] != 2  :
        return abort(403)
    else: 
        email=session["username"]
        id=execute_query(f"SELECT teacher_id FROM teachers WHERE email='{email}'")[0][0]
        session["id"]=id

        teacher_info=[]
        ti=execute_query(f"SELECT * FROM teachers WHERE teacher_id={id}")
        for t in ti:
            teacher=namedtuple("Teacher", ['t_id','t_name', 'email','img'])
            teacher.t_id=t[0]
            teacher.t_name=t[1]
            teacher.email=t[2]
            teacher.img=t[4]
            teacher_info.append(teacher)

        course_info=[]
        ci=execute_query(f"""
            SELECT  * FROM active_courses 
            WHERE teacher_id={id}""")
        for c in ci:
            course=namedtuple("Courses", ['c_id','c_name', 'avg_grade' ])
            course.c_id=c[0]
            course.c_name=c[1]
            course.avg_grade=Teacher.avg(c[0])
            course_info.append(course)
            
            
        return render_template("teacher_info.html", teacher=teacher_info, course_info=course_info)

@app.route('/teacher/update', methods=['GET', 'POST'])
def teacher_update():
    if request.method=="GET":
        email=session["username"]
        name=execute_query(f"SELECT name FROM teachers WHERE email='{email}'")[0][0]
        return render_template ("teacher_update.html" ,email=email, s_name=name)
    else:
        n_email=request.form["email"]
        o_email=session["username"]
        Teacher.update(n_email=n_email,o_email=o_email)
        session.clear()
        session["username"]=f"{n_email}"
        session["role"]=2
        return redirect(url_for("teacher_info"))
    
@app.route('/teacher/upload', methods=['GET', 'POST'])
def teacher_upload():
    if request.method == 'POST':
        file = request.files['img']
        name=request.form["name"]
        if file:
            filename = file.filename
            file.save(os.path.join('static/img/teachers', filename))
            execute_query(f"UPDATE teachers SET image ='{filename}' WHERE name ='{name}'")
            return redirect(url_for("teacher_info"))

@app.route('/teacher/course/<teacher_id>/<course_id>', methods=['GET', 'POST'])
def teacher_course_info(teacher_id, course_id):
    course_info=[]
    ci=execute_query(f"""
            SELECT  * FROM active_courses 
            WHERE course_id={course_id} AND teacher_id={teacher_id}""")
    for c in ci:
        course=namedtuple("Courses", ['c_id','c_name','date', 'avg_grade','per_presence' ])
        course.c_id=c[0]
        course.c_name=c[1]
        course.date=c[3]
        course.avg_grade=Teacher.avg(c[0])
        course.per_presence=per_presence_course(c[0])
        course_info.append(course)
    
    student_info=[]
    si=execute_query(f"""
        SELECT students_courses.student_id, students_courses.course_id, students_courses.grade, students.name 
        FROM students_courses  
        JOIN students WHERE students_courses.student_id=students.student_id 
        AND students_courses.course_id={course_id} """)
    for s in si:
        student=namedtuple("Student", ['s_id','s_name', 'grade', 'per_presence'])
        student.s_id=s[0]
        student.s_name=s[3]
        student.grade=s[2]
        student.per_presence=per_presence_by_id_course(s[0], s[1])

        student_info.append(student)
    
    return render_template("teacher_course.html" , student_info=student_info, course_info=course_info )

    
    

@app.route('/teacher/grade/<course_id>', methods=['GET', 'POST'])
def teacher_grade(course_id):
    course_name=execute_query(f"SELECT name FROM active_courses WHERE course_id={course_id}")[0][0]
    b_info=[session["id"], course_id, course_name]
    grades_lst=[]
    info=execute_query(f"""
        SELECT students_courses.student_id, students_courses.course_id, students_courses.grade, students.name FROM students_courses
        JOIN students WHERE students_courses.student_id=students.student_id 
        AND students_courses.course_id = {course_id}""")
    for s in info:
        student=namedtuple("Student", ['s_id','c_id','s_name', 'grade'])
        student.s_id=s[0]
        student.c_id=s[1]
        student.s_name=s[3]
        student.grade=s[2]
        grades_lst.append(student)
    
    
    return render_template("teacher_grade.html" , grades_lst=grades_lst, b_info=b_info )
    

@app.route('/set_grade', methods=['GET', 'POST'])
def set_grade():
    s_id=request.form["student_id"]
    c_id=request.form["course_id"]
    grade=request.form["grade"]
    
    set=execute_query(f"""
        UPDATE students_courses
        SET grade = {grade}
        WHERE course_id ={c_id} AND student_id={s_id}""")
    return redirect(url_for(f"teacher_grade", course_id=c_id))


   

#course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    courses=PublicCourse.show_info()
    return render_template("add_course.html", courses=courses)
    

@app.route('/add_active_course', methods=['GET', 'POST'])
def add_active_course():
    # if session['role']!= 3:
    #         return abort(403)
    teachers = execute_query("SELECT teacher_id , name FROM teachers")
    courses=execute_query("SELECT name FROM courses")
    a_courses = execute_query("""
        SELECT active_courses.course_id ,active_courses.name ,active_courses.date ,teachers.name 
        FROM active_courses 
        left JOIN teachers 
        on active_courses.teacher_id=teachers.teacher_id
        ORDER BY active_courses.name ASC """)

    teachers_lst = []
    courses_lst=[]
    a_courses_lst = []
    # what SQL Syntax do i need to use to get courses.name and teachers. name when i only have courses_teachers_id
    for teacher_tuple in teachers:
        teacher = namedtuple("Teacher", ['id', 'name'])
        teacher.id = teacher_tuple[0]
        teacher.name = teacher_tuple[1]
        teachers_lst.append(teacher)

    for tuple in courses:
        courses_lst.append(tuple[0])

    for course_tuple in a_courses:
        course = namedtuple("Course", ['id','c_name', 't_name','date'])
        course.id = course_tuple[0]
        course.c_name = course_tuple[1]
        course.date=course_tuple[2]
        course.t_name = course_tuple[3]
        a_courses_lst.append(course)

    if request.method == 'GET':
        return render_template("add_active_course.html", teachers_lst=teachers_lst, a_courses_lst=a_courses_lst, courses_lst=courses_lst)
    else:
        teacher_id = request.form["teacher_id"]
        course_name = request.form["course_name"]
        start_date=request.form["start_date"]
        file = request.files['file']

        if file:
            filename = file.filename
            file.save(os.path.join('static/files', filename))

        if start_date == "":
            msg = "Please choose start date for this course and try again"
            return render_template("add_active_course.html", teachers_lst=teachers_lst, msg=msg)
        if teacher_id == "":
            msg = "Please choose teacher for this course and try again"
            return render_template("add_active_course.html", teachers_lst=teachers_lst, msg=msg)
        elif course_name == "":
            msg = "Please enter course name and try again"
            return render_template("add_active_course.html", teachers_lst=teachers_lst, msg=msg)
        else:
            #teacher_id=execute_query(f"SELECT teachers_id FROM teachers WHERE name={teacher_name}")

            try:
                Course.add(course_name, teacher_id,start_date,file)
            except:
                msg="something went wrong, please try again."
            else:
                msg = "The Course Was Added Successfully !"
                
            return redirect(url_for("add_active_course"))

@app.route('/admin/update/active_course/<course_id>', methods=['GET', 'POST'])
def update_active_course(course_id):
    if request.method=="GET":

        a_courses = execute_query(f"""
            SELECT active_courses.course_id ,active_courses.name ,active_courses.date ,teachers.name 
            FROM active_courses 
            left JOIN teachers 
            on active_courses.teacher_id=teachers.teacher_id
            WHERE active_courses.course_id={course_id}
            ORDER BY active_courses.name ASC """)
        a_courses_lst = []
        
        for course_tuple in a_courses:
            course = namedtuple("Course", ['id','c_name', 't_name','date'])
            course.id = course_tuple[0]
            course.c_name = course_tuple[1]
            course.date=course_tuple[2]
            course.t_name = course_tuple[3]
            a_courses_lst.append(course)


        return render_template("active_course_update.html", a_courses_lst=a_courses_lst)
    else:
        date=request.form["start_date"]
        file=request.files["file"]

        if file:
            filename = file.filename
            file.save(os.path.join('static/files', filename))
            
        a=Course.update(course_id, filename, date)  
        return redirect(url_for("add_active_course"))  
    

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




@app.route('/attendance/<course_id>', methods=['GET','POST'])
def atten_date(course_id):
    
    if request.method== "GET":
        return render_template("students_attendance.html" ,course_id=course_id)
    else:
        id=request.form['course_id']
        date=request.form['local_date']
        return redirect(url_for("attendance",id=id, atten_date=date))

@app.route('/attendance/<id>/<atten_date>', methods=['GET', 'POST'])
def attendance(id,atten_date):
    if request.method=='GET':
        try:
            info=Attendance.show_by_id_date_info(course_id=id, atten_date=atten_date)
            if info==[]:
                raise ValueError
        except:
            student_info=execute_query(f"SELECT student_id FROM students_courses WHERE course_id={id}")
            for student in student_info:
                Attendance.add(student_id=student[0], course_id=id, atten_date=atten_date)
                
        attendance_lst=Attendance.show_by_id_date_lst(course_id=id, atten_date=atten_date)
        return render_template("students_attendance.html", attendance_lst=attendance_lst ,atten_date=atten_date,course_id=id)
    
    else:
        id=id
        a_date=request.form['local_date']
        return redirect(url_for("attendance",id=id, atten_date=a_date))
    
@app.route('/set_atten', methods=['GET', 'POST'])
def set():
    if request.method=="POST":
        course_id =request.form["course_id"]
        date =request.form["date"]
        student_id =request.form["student_id"]
        present = request.form['my_radio']

        set_i=execute_query(f"""
        UPDATE attendance
        SET present = '{present}'
        WHERE course_id ={course_id} AND student_id={student_id} AND date='{date}'
        """)

    return redirect(url_for("attendance" ,atten_date=date, id=course_id ))

@app.route('/name_attendance/<course_id>', methods=['GET', 'POST'])
def name_attendance(course_id):
    if request.method=='GET':
        
        students_lst=[]
        info=execute_query(f"""
            SELECT students_courses.course_id, students_courses.student_id , students.name, active_courses.name AS course_name FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
			JOIN active_courses on active_courses.course_id={course_id}
            WHERE students_courses.course_id={course_id}""")
        
        for s_tuple in info:
            s=namedtuple("Student", ['c_id','c_name','s_id', 's_name'])
            s.c_id=s_tuple[0]
            s.s_id=s_tuple[1]
            s.s_name=s_tuple[2]
            s.c_name=s_tuple[3]
            students_lst.append(s)

        return render_template("name_attendance.html", students_lst=students_lst)
       
    else: 
        students_lst=[]   
        student_id=request.form["name"]
        atten_date=request.form["date"]

        info=execute_query(f"""
            SELECT students_courses.course_id, students_courses.student_id , students.name, active_courses.name AS course_name FROM students_courses
            JOIN students on students_courses.student_id=students.student_id
			JOIN active_courses on active_courses.course_id={course_id}
            WHERE students_courses.course_id={course_id}""")
        
        for s_tuple in info:
            s=namedtuple("Student", ['c_id','c_name','s_id', 's_name'])
            s.c_id=s_tuple[0]
            s.s_id=s_tuple[1]
            s.s_name=s_tuple[2]
            s.c_name=s_tuple[3]
            students_lst.append(s)

        raw_info=Attendance.show_by_student_date(course_id=course_id, student_id=student_id, atten_date=atten_date)
        results=Attendance.show_by_student_date_lst(course_id=course_id, student_id=student_id, atten_date=atten_date)

        if raw_info==[]:
            msg="No such records, pleas try a different date "
            results=[]
            return render_template("name_attendance.html", students_lst=students_lst ,results=results ,atten_date=atten_date, msg=msg)
        return render_template("name_attendance.html", students_lst=students_lst, results=results, atten_date=atten_date)

@app.route('/submit', methods=['POST'])
def submit():
    pass    
       
            
      
    
      

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


@app.route('/delete_active_course/<course_id>')
def delete_course(course_id):
    delete=execute_query(f"DELETE FROM active_courses WHERE course_id={course_id}")
    return redirect(url_for("add_active_course"))
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

# @app.route('/teacher/<techer_id>/<course_id>', methods=['POST'])
# def method_name():
#     pass
    
            
    # for i in range(len(courses)):
    #     info[f"{course[0][i]}"]={"students":[f"""
    #     SELECT students_courses.student_id,students.name, students_corses.grade FROM students
    #     LEFT JOIN students_courses 
    #     ON students_courses.student_id
    #     WHERE students_courses.course_id={course[1][i]}"""]}
    #     #makes no sense!
@app.route('/listall', methods=['GET', 'POST'])
def listall():
    result= Student.json_result()
    return result

@app.route('/student_search', methods=['GET', 'POST'])
def student_search():
    name=request.form["name"]
    try:
        results=Student.show_all_search(name)
        if results != []:
            return render_template("show_students.html", students=results, back="Show All")
        return redirect(url_for("all_students"))
    except:
        return redirect(url_for("all_students"))

@app.route('/teacher_search', methods=['GET', 'POST'])
def teacher_search():
    name=request.form["name"]
    try:
        results=Teacher.show_all_search(name)
        if results != []:
            return render_template("show_teachers.html", teachers=results, back="Show All")
        return redirect(url_for("all_teachers"))
    except:
        return redirect(url_for("all_teachers"))    

@app.route('/course_search', methods=['GET', 'POST'])
def course_search():
    key=request.form["key"]
    courses=[]
    course=execute_query(f"""
        SELECT name, description FROM courses WHERE courses.name  LIKE '%{key}%'""")
    for course_tuple in course:
        course = namedtuple("Course", ['course_name', 'desc'])
        course.course_name = course_tuple[0]
        course.desc = course_tuple[1]
        courses.append(course)
    try:
        if courses != []:
            return render_template("show_courses.html", courses=courses, back="Show All")
        return redirect(url_for("show_courses"))
    except:
        return redirect(url_for("show_courses")) 

@app.route('/admin/delete/active_course/<course_id>', methods=['GET', 'POST'])
def delete_active_course(course_id):
    
    return redirect(url_for("add_active_course"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
