import os
import sys
import psycopg2
from datetime import datetime
import pymongo 
import random
from bson.son import SON

client = pymongo.MongoClient("mongodb+srv://ogencer2:iWMOdvjfmgaKTLmO@cluster0.iez4s.mongodb.net/BayDB?retryWrites=true&w=majority")
mydb = client["BayDB"]
mycol = mydb["BayDB"]
#test = mycol.find_one()
#print(test)
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

def createTask(taskname, assignedto, repeat, usernotes, cursor=cur):
    exists = 'false'
    groupid = 71 ##need to chnage
    taskid = random.randrange(1,2147483647) #id range
    taskname = "'" + taskname + "'"
    assignedto = "'" + assignedto + "'"
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

def getRecurringTasks(curs=cur):
    query = 'SELECT * FROM recurring_table;'
    cur.execute(query)
    reccuring = cur.fetchall()
    for i in reccuring:
        sched = i[2].split(" ")[0]
        if (sched == "Daily"):
            print(i)
            createTask(i[1], i[3], "No", "", cursor=curs)

getRecurringTasks()