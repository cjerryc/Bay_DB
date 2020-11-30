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

def useFunct(tID, cur=cur, conn=conn):
    now = datetime.now()
    date = str(now.strftime("%m/%d/%Y"))
    time = str(now.strftime("%H:%M"))
    date = "'" + date + "'"
    time = "'" + time + "'"
    query = 'SELECT upRecurrTask(%s, %s, %s);' %(tID, date, time)
    cur.execute(query)
    conn.commit()

def getRecurringTasks(curs=cur):
    query = 'SELECT * FROM recurring_table;'
    cur.execute(query)
    reccuring = cur.fetchall()
    for i in reccuring:
        sched = i[2].split(" ")[0]
        day = None
        if (len(i[2].split(" ")) > 1):
            day = i[2].split(" ")[1]
            day = day.replace('(', '')
            day = day.replace(')', '')
        if (sched == "Daily"):
            useFunct(i[0])  
        if (sched == "Weekly"):
            if (datetime.today().strftime('%A') == day):
                useFunct(i[0]) 

getRecurringTasks()