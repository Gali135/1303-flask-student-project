from setup_db import create_tables, create_fake_data, execute_query
import requests 
#pytest example
def test_db():
    #create_tables()
    #create_fake_data()
    num=int(execute_query("SELECT COUNT(id) FROM students")[0][0])
    #The execute query returns a list of tuples so we want to get the first object from the forst tuple hennce the [0][0]
    assert num==80
def test_registration():
    course_id=4
    r=requests.get("http://127.0.0.1:5000/register/1/3")
    if r.status_code==200:
        r=requests.get("http://127.0.0.1:5000/registerations/1")
        name=requests.get(f"http://127.0.0.1:5000/registerations/course/{course_id}").json()[0][0]
        assert r.text.find(name)!=-1
        #find will return the index if there's no index it will return -1