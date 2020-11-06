import os
import psycopg2

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
    print(query)
    cursor.execute(query)
    return cur.fetchone()

def logUserIn(username, passcode, cursor=cur):
    username = "'" + username + "'"
    passcode = "'" + passcode + "'"
    query = 'SELECT firstname, lastname, email FROM users WHERE users.username = %s AND users.passcode = %s;' % (username, passcode)
    print(query)
    cursor.execute(query)
    return cur.fetchone()

def createUser(username, firstname, lastname, email, passcode, cursor=cur):
    username = "'" + username + "'"
    firstname = "'" + firstname + "'"
    lastname = "'" + lastname + "'"
    email = "'" + email + "'"
    passcode = "'" + passcode + "'"
    query = 'INSERT INTO users(username, firstname, lastname, email, passcode) VALUES (%s, %s, %s, %s, %s);' % (username, firstname, lastname, email, passcode)
    print(query)
    cursor.execute(query)
    conn.commit()
    #return cursor.fetchone()

def createTask(taskname):
    taskname = "'" + taskname + "'"
    username = "'none'"
    status = "'pending'"
    date = "'none'"
    time = "'none'"
    query = 'INSERT INTO tasks(taskname, username, status, date, time) VALUES (%s, %s, %s, %s, %s);' % (taskname, username, status, date, time)
    print("\nTESTING")
    print(query)
    print("TESTING\n")
    cursor.execute(query)
    conn.commit()
    #return cursor.fetchone()

