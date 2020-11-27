import os
import psycopg2
from datetime import datetime
import pymongo
import random
current_username = "unknown"


client = pymongo.MongoClient("mongodb+srv://ogencer2:iWMOdvjfmgaKTLmO@cluster0.iez4s.mongodb.net/BayDB?retryWrites=true&w=majority")
mydb = client["BayDB"]
mycol = mydb["BayDB"]
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

def logUserOut():
    global current_username
    current_username = "unknown"

def getUser(username, cursor=cur):
    username = "'" + username + "'"
    query = 'SELECT firstname, lastname FROM users WHERE users.username = %s;' % username
    cursor.execute(query)
    return cur.fetchone()
    
def getUserInfo(cursor = cur):
    username = "'" + current_username + "'"
    query = 'SELECT * FROM users WHERE users.username = %s;' % username
    cursor.execute(query)
    return cur.fetchone()

def getTasks(cursor = cur):
    cur.execute("SELECT * FROM tasks_table;")
    return cur.fetchall()

def tasksExists(taskname, cursor = cur):
    query = 'SELECT taskname FROM tasks_table WHERE tasks_table.taskname = %s;'%taskname
    cur.execute(query)
    return cur.fetchall()  

def searchTasks(taskname, cursor = cur):
    taskname = "'%" + taskname + "%'"
    query = 'SELECT * FROM tasks_table WHERE (tasks_table.taskname LIKE %s) OR (tasks_table.doneby LIKE %s) OR (tasks_table.assignedto LIKE %s) OR (tasks_table.status LIKE %s) OR (tasks_table.date LIKE %s) OR (tasks_table.time LIKE %s);' % (taskname, taskname, taskname, taskname, taskname, taskname)
    cur.execute(query)
    return cur.fetchall()

def getGroupName(groupid, cursor = cur):
    groupid = "'" + groupid + "'"
    query = 'SELECT groupname FROM groups_table WHERE groupid = %s;' % (groupid)
    cur.execute(query)
    return cur.fetchall()

def getGroupMembers(groupid, cursor = cur):
    groupid = "'" + groupid + "'"
    query = 'SELECT firstname, lastname FROM users WHERE groupid = %s;' % (groupid)
    cur.execute(query)
    return cur.fetchall()

def checkGroupID(usrnm, cursor=cur):
    usrnm = "'" + usrnm + "'"
    query = 'Select Groupid FROM groups_table WHERE %s = ANY (Username);' %usrnm
    cursor.execute(query)
    return (int(cursor.fetchone()[0]))

def deleteTask(task, cursor = cur):
    taske = "'" + task + "'"
    #select = 'SELECT * FROM tasks_table WHERE taskname = %s;' %taske
    #cursor.execute(select)
    #slct = cursor.fetchone()
    #print(slct)
    #tskname = "'" + slct[0] + "'"
    #usrname = "'" + slct[1] + "'"
    #stts = "'" + slct[2] + "'"
    #dt = "'" + slct[3] + "'"
    #tm = "'" + slct[4] + "'"
    #insrt = 'INSERT INTO tasks(taskname, username, status, date, time) VALUES (%s, %s, %s, %s, %s);' % (tskname, usrname, stts, dt, tm)
    #cursor.execute(insrt)
    #conn.commit()
    query = 'DELETE FROM tasks_table WHERE taskname = %s;' %taske
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
    global current_username
    current_username = username
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

def createTask(taskname, assignedto, repeat, usernotes, cursor=cur):
    global current_username
    exists = tasksExists("'" + taskname + "'")
    if not exists:
        exists = 'false'
        groupid = 71 ##need to chnage
        taskid = random.randrange(1,2147483647) #id range
        taskname = "'" + taskname + "'"
        assignedto = "'" + assignedto + "'"
        username = "'" + current_username + "'"
        #need to get groupid select from group table
        #groupid = "'" + groupid + "'"
        status = "'incomplete'"
        now = datetime.now()
        date = str(now.strftime("%m/%d/%Y"))
        time = str(now.strftime("%H:%M"))
        #date = 'none'
        #time = 'none'
        usernotes = "'" + usernotes + "'"
        date = "'" + date + "'"
        time = "'" + time + "'"
        repeat = "'" + repeat + "'"
        query = 'INSERT INTO tasks_table(taskid, taskname, date, time, status, assignedto, completeddate, completedtime, doneby, groupid, subtasks, materials, notes) VALUES (%s, %s, %s, %s, %s, %s, NULL, NULL, NULL, %s, NULL, NULL, %s);' % (taskid, taskname, date, time, status, assignedto, groupid, usernotes)
        cursor.execute(query)
        conn.commit()
        print(repeat)
        if "No" not in repeat:
            query = 'INSERT INTO recurring_table(taskid,taskname,repeattime,assignedto,groupid,subtasks,materials,notes) VALUES ( %s, %s, %s, %s, %s,NULL, NULL, %s) ;'% (taskid, taskname, repeat, assignedto, groupid, usernotes)
            cursor.execute(query)
            conn.commit()
    else:
        "<h1>Task already exists! Enter a new task.</h1>"
    
    return exists
def completeTask(taskname, cursor=cur):
    global current_username
    exists = tasksExists("'" + taskname + "'")
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M")

    mongo_template = { "history_id": int(datetime.now().timestamp()),
          "task_id": 4,
          "group_id": checkGroupID(current_username),
          "taskname": taskname,
          "username": current_username,
          "date": date,
          "time": time,
          "was_assigned": True,
          "subtasks": ["hi", "lol", "love"]}

    if exists:
        exists = 'true' 
        taskname = "'" + taskname + "'"
        username = "'" + current_username + "'"
        status = "'complete'"
        date = "'" + date + "'"
        time = "'" + time + "'"
        query = 'UPDATE tasks_table SET doneby = %s, status = %s, completeddate = %s, completedtime = %s WHERE taskname = %s;' % (username, status, date, time, taskname)
        cursor.execute(query)
        conn.commit()
        mycol.insert_one(mongo_template)
    else:
        exists = 'false'
    
    return exists

def updateTask(taskname, cursor=cur):
    global current_username
    exists = tasksExists("'" + taskname + "'")
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M")

    mongo_template = { "history_id": int(datetime.now().timestamp()),
          "task_id": 4,
          "group_id": checkGroupID(current_username),
          "taskname": taskname,
          "username": current_username,
          "date": date,
          "time": time,
          "was_assigned": True,
          "subtasks": ["hi", "lol", "love"]}

    if exists:
        exists = 'true' 
        taskname = "'" + taskname + "'"
        username = "'" + current_username + "'"
        status = "'complete'"
        date = "'" + date + "'"
        time = "'" + time + "'"
        query = 'UPDATE tasks_table SET doneby = %s, status = %s, completeddate = %s, completedtime = %s WHERE taskname = %s;' % (username, status, date, time, taskname)
        cursor.execute(query)
        conn.commit()
        mycol.insert_one(mongo_template)
    else:
        exists = 'false'
    
    return exists
    