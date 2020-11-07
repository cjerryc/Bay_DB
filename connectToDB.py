import os
import psycopg2
from datetime import datetime

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except:
    conn = psycopg2.connect(
        host="ec2-52-200-134-180.compute-1.amazonaws.com",
        database="d6ehld1vcv1vv1",
        user="vuxncunnoferwp",
        password="bab2d1e1b712cbc8c6a16c50213d0d5888c7b53c74ea961aba4a708f55e36115")
cur = conn.cursor()

def getUser(username, cursor=cur):
    username = "'" + username + "'"
    query = 'SELECT firstname, lastname FROM users WHERE users.username = %s;' % username
    cursor.execute(query)
    return cur.fetchone()

def getTasks(cursor = cur):
    cur.execute("SELECT * FROM active_tasks;")
    return cur.fetchall()

def tasksExists(taskname, cursor = cur):
    query = 'SELECT taskname FROM active_tasks WHERE active_tasks.taskname = %s;'%taskname
    cur.execute(query)
    return cur.fetchall()  

def searchTasks(taskname, cursor = cur):
    taskname = "'%" + taskname + "%'"
    query = 'SELECT * FROM active_tasks WHERE (active_tasks.taskname LIKE %s) OR (active_tasks.username LIKE %s) OR (active_tasks.status LIKE %s) OR (active_tasks.date LIKE %s) OR (active_tasks.time LIKE %s);' % (taskname, taskname, taskname, taskname, taskname)
    cur.execute(query)
    return cur.fetchall()

def deleteTask(task, cursor = cur):
    taske = "'" + task + "'"
    select = 'SELECT * FROM active_tasks WHERE taskname = %s;' %taske
    cursor.execute(select)
    slct = cursor.fetchone()
    print(slct)
    tskname = "'" + slct[0] + "'"
    usrname = "'" + slct[1] + "'"
    stts = "'" + slct[2] + "'"
    dt = "'" + slct[3] + "'"
    tm = "'" + slct[4] + "'"
    insrt = 'INSERT INTO tasks(taskname, username, status, date, time) VALUES (%s, %s, %s, %s, %s);' % (tskname, usrname, stts, dt, tm)
    cursor.execute(insrt)
    conn.commit()
    query = 'DELETE FROM active_tasks WHERE taskname = %s;' %taske
    cursor.execute(query)
    if cursor.statusmessage == "DELETE 0":
        conn.commit()
        print(cursor.statusmessage)
        return 'false'
    else:
        conn.commit()
        print(cursor.statusmessage)
        return 'true'
    
def logUserIn(username, passcode, cursor=cur):
    username = "'" + username + "'"
    passcode = "'" + passcode + "'"
    query = 'SELECT firstname, lastname, email FROM users WHERE users.username = %s AND users.passcode = %s;' % (username, passcode)
    cursor.execute(query)
    return cur.fetchone()

def createUser(username, firstname, lastname, email, passcode, cursor=cur):
    username = "'" + username + "'"
    firstname = "'" + firstname + "'"
    lastname = "'" + lastname + "'"
    email = "'" + email + "'"
    passcode = "'" + passcode + "'"
    query = 'INSERT INTO users(username, firstname, lastname, email, passcode) VALUES (%s, %s, %s, %s, %s);' % (username, firstname, lastname, email, passcode)
    cursor.execute(query)
    conn.commit()
    #return cursor.fetchone()

def createTask(taskname, username, cursor=cur):
    exists = tasksExists("'" + taskname + "'")

    if not exists or exists == 'false' :
        exists = 'false'
        taskname = "'" + taskname + "'"
        username = "'" + username + "'"
        status = "'pending'"
        now = datetime.now()
        date = str(now.strftime("%m/%d/%Y"))
        time = str(now.strftime("%H:%M"))
        #date = 'none'
        #time = 'none'
        date = "'" + date + "'"
        time = "'" + time + "'"
        query = 'INSERT INTO active_tasks(taskname, username, status, date, time) VALUES (%s, %s, %s, %s, %s);' % (taskname, username, status, date, time)
        cursor.execute(query)
        conn.commit()
    else:
        "<h1>Task already exists! Enter a new task.</h1>"
    
    return exists
    
    
    #return cursor.fetchone()


def updateTask(taskname, username, date, time, cursor=cur):
    exists = tasksExists("'" + taskname + "'")

    if exists:
        exists = 'true' 
        taskname = "'" + taskname + "'"
        username = "'" + username + "'"
        status = "'complete'"
        date = "'" + date + "'"
        time = "'" + time + "'"
        query = 'UPDATE active_tasks SET username = %s, status = %s, date = %s, time = %s WHERE taskname = %s;' % (username, status, date, time, taskname)
        cursor.execute(query)
        conn.commit()
    else:
        exists = 'false'
    
    return exists
    
    
    #return cursor.fetchone()