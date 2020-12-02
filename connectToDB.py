import os
import sys
import psycopg2
from datetime import datetime
import pymongo 
import random
from bson.son import SON
import redis
import json
current_username = "unknown"
current_groupid = 0
current_taskid = 0
client = pymongo.MongoClient("mongodb+srv://ogencer2:iWMOdvjfmgaKTLmO@cluster0.iez4s.mongodb.net/BayDB?retryWrites=true&w=majority")
mydb = client["BayDB"]
mycol = mydb["BayDB"]
mysub = mydb["Subtasks"]
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
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
try:
    db=redis.from_url(os.environ['REDISCLOUD_URL'])
except:
    print("Local Use!")


def logUserOut():
    global current_username
    global current_groupid 
    try:
        db.set('current_username', "unknown")
        db.set('current_groupid', 0)
    except:
        current_username = "unknown"
        current_groupid = 0

def getUser(username, cursor=cur):
    username = "'" + username + "'"
    query = 'SELECT firstname, lastname FROM users WHERE users.username = %s;' % username
    cursor.execute(query)
    return cur.fetchone()
    
def getUsernames(groupid, cursor=cur):
    a = int(groupid)
    query = "SELECT username FROM users WHERE groupid::int = %i;" %a
    cursor.execute(query)
    return cur.fetchall()

def getUserInfo(cursor = cur):
    global current_username
    try:
        username = "'" + db.get('current_username') + "'"
    except:
        username = "'" + current_username + "'"
    query = 'SELECT * FROM users WHERE users.username = %s;' % username
    cursor.execute(query)
    return cur.fetchone()

def getTasks(cursor = cur):
    global current_groupid 
    a = int(current_groupid)
    query = "SELECT * FROM tasks_table WHERE groupid::int = %i;" %a 
    cur.execute(query)
    print(cur.statusmessage)
    return cur.fetchall()

def getTaskNames(cursor = cur):
    global current_groupid
    a = int(current_groupid)
    query = "SELECT taskname FROM tasks_table WHERE groupid::int = %i;" %a 
    cur.execute(query)
    return cur.fetchall()

def getRecurringTaskNames(cursor = cur):
    global current_groupid
    a = int(current_groupid)
    query = "SELECT taskname FROM recurring_table WHERE groupid::int = %i;" %a 
    cur.execute(query)
    return cur.fetchall()

def tasksExists(taskname, cursor = cur):
    global current_groupid 
    print(current_groupid)
    taskname = "'" + taskname + "'"
    a = int(current_groupid)
    query = 'SELECT taskid FROM tasks_table WHERE tasks_table.taskname = %s AND groupid::int = %i;'% (taskname, a)
    cur.execute(query)
    return cur.fetchall()  

def tasksRecurring(taskname, cursor = cur):
    global current_groupid 
    print(current_groupid)
    taskname = "'" + taskname + "'"
    a = int(current_groupid)
    query = 'SELECT taskname FROM recurring_table WHERE taskname = %s AND groupid::int = %i;'% (taskname, a)
    cur.execute(query)
    return cur.fetchall()  

def deleteRecurring(taskname, cursor = cur):
    global current_groupid
    print(current_groupid)
    taskname = "'" + taskname + "'"
    a = int(current_groupid)
    query = 'DELETE FROM recurring_table WHERE taskname = %s AND groupid::int = %i;'% (taskname, a)
    cur.execute(query)  
    conn.commit()

def searchTasks(taskname, cursor = cur):
    global current_groupid
    taskname = "'%" + taskname + "%'"
    a = int(current_groupid)
    query = 'SELECT * FROM tasks_table WHERE groupid::int = %i AND ((tasks_table.taskname LIKE %s) OR (tasks_table.doneby LIKE %s) OR (tasks_table.assignedto LIKE %s) OR (tasks_table.status LIKE %s) OR (tasks_table.date LIKE %s) OR (tasks_table.time LIKE %s));' % (a, taskname, taskname, taskname, taskname, taskname, taskname)
    cur.execute(query)
    return cur.fetchall()

def searchHistory(taskname, date_created, assignedto, date_completed, doneby, cursor = cur):
    global current_groupid
    thisdict =	{
        "taskname": taskname,
        "date_created": date_created,
        "assignedto": assignedto,
        "date_completed": date_completed,
        "doneby": doneby
    }
    boop = {}
    for item in thisdict.keys():
        if len(thisdict[item]) != 0:
            boop[item] = "'%" + thisdict[item] + "%'"
    querydict = {
        "taskname": 'SELECT * FROM history_table WHERE groupid::int = %i AND taskname LIKE %s',
        "date_created": 'SELECT * FROM history_table WHERE groupid::int = %i AND date LIKE %s',
        "assignedto": 'SELECT * FROM history_table WHERE groupid::int = %i AND assignedto LIKE %s',
        "date_completed": 'SELECT * FROM history_table WHERE groupid::int = %i AND completeddate LIKE %s',
        "doneby": 'SELECT * FROM history_table WHERE groupid::int = %i AND doneby LIKE %s'
    }
    query = []
    items  = []
    intersect = ' INTERSECT '

    for item in boop.keys():
        query.append(querydict[item])
        items.append(int(current_groupid))
        items.append(boop[item])
    items = tuple(items)
    if len(query) == 0:
        allquery = 'SELECT * FROM history_table WHERE groupid::int = %i;' % current_groupid
        cur.execute(allquery)
        return cur.fetchall()
    stringquery = ''
    for index in range(len(query) - 1):
        stringquery = stringquery + query[index] + intersect
    stringquery = stringquery + query[len(query) - 1]
    
    print(items)
    finalquery = ((stringquery + ';') % items)
    print(stringquery)
    print(finalquery)
    cur.execute(finalquery)
    return cur.fetchall() 
    

def getSubtasks(taskname, cursor = cur):
    global current_groupid 
    taskname = "'" + taskname + "'"
    a = int(current_groupid)
    query = 'SELECT subtasks FROM tasks_table WHERE taskname = %s AND groupid::int = %i;'% (taskname, a)
    cur.execute(query)
    return cur.fetchall()  


def getGroupName(groupid, cursor = cur):
    global current_groupid
    current_groupid = groupid
    groupid = "'" + groupid + "'"
    query = 'SELECT groupname FROM groups_table WHERE groupid = %s;' % (groupid)
    cur.execute(query)
    return cur.fetchall()

def getGroupMembers(groupid, cursor = cur):
    global current_groupid
    current_groupid = groupid
    groupid = "'" + groupid + "'"
    query = 'SELECT firstname, lastname FROM users WHERE groupid = %s;' % (groupid)
    cur.execute(query)
    return cur.fetchall()

def checkGroupID(usrnm, cursor=cur):
    usrnm = "'" + usrnm + "'"
    #query = 'SELECT groupid FROM groups_table WHERE %s = ANY (username);' %usrnm
    query = 'SELECT groupid FROM users WHERE username = %s ;' %usrnm
    cur.execute(query)
    return cur.fetchall()

def getTaskIDs( cursor=cur):
    query = 'SELECT taskid FROM task_table;' 
    cur.execute(query)
    return cur.fetchall()

def joinGroup(groupid, cursor=cur, conn=conn):
    global current_username
    global current_groupid 
    current_groupid = int(groupid)
    try:
        username = "'" + db.get('current_username') + "'"
    except:
        username = "'" + current_username + "'"
    groupid = str(groupid)
    updateUser = 'UPDATE users SET groupid = %s WHERE username = %s;' %(groupid, username)
    cur.execute(updateUser)
    conn.commit()

def leaveGroup(cursor=cur, conn=conn):
    global current_username
    global current_groupid
    current_groupid = 0
    try:
        username = "'" + db.get('current_username') + "'"
    except:
        username = "'" + current_username + "'"
    updateUser = 'UPDATE users SET Groupid = %s WHERE Username = %s;' %('null', username)
    print(updateUser)
    cur.execute(updateUser)
    conn.commit()

def createGroup(groupName, groupid):
    groupName = "'" + str(groupName) + "'" 
    createG = 'INSERT INTO groups_table (groupid, groupname) VALUES (%s, %s);' %(groupid, groupName)
    cur.execute(createG)
    joinGroup(groupid)

def deleteTask(task, cursor = cur):
    global current_groupid
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
    a = int(current_groupid)
    query = 'DELETE FROM tasks_table WHERE taskname = %s AND groupid::int = %i;'% (taske, a)
    cursor.execute(query)

    if cursor.statusmessage == "DELETE 0":
        conn.commit()
        print(cursor.statusmessage)
        return 'false'
    else:
        conn.commit()
        print(cursor.statusmessage)
        recurring = tasksRecurring(task)
        if(recurring):
            #print(recurring)
            deleteRecurring(task)
        return 'true'

def logUserIn(username, passcode, cursor=cur):
    global current_username
    global current_groupid
    try:
        db.set('current_username',username)
        current_username = username
    except:
        current_username = username

    group_id = checkGroupID(current_username)
    current_groupid = group_id

    try:
        group_id = " ".join(list(group_id[0]))
    except:
        group_id = 0

    group_id = int(group_id)
    try:
        db.set('current_groupid',group_id)
        current_groupid = group_id
    except:
        current_groupid = group_id
    username = "'" + username + "'"
    passcode = "'" + passcode + "'"
    query = 'SELECT firstname, lastname, email FROM users WHERE users.username = %s AND users.passcode = %s;' % (username, passcode)
    cursor.execute(query)
    return cur.fetchone()


def findAssignment(taskname, cursor=cur):
    global current_groupid
    try:
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    taskname = "'" + taskname + "'"
    a = int(current_groupid)
    query = 'SELECT assignedto FROM tasks_table WHERE taskname = %s AND groupid::int = %i;'% (taskname, a)
    cursor.execute(query)
    return cur.fetchone()

def findTaskID(taskname, cursor=cur):
    global current_groupid
    try:
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    taskname = "'" + taskname + "'"
    a = int(current_groupid)
    query = 'SELECT taskid FROM tasks_table WHERE taskname = %s AND groupid::int = %i;'% (taskname, a)
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
    global current_groupid
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    exists = tasksExists(taskname)
    if not exists:
        exists = 'false'
        groupid = current_groupid ##need to chnage
        taskid = random.randrange(1,2147483647) #id range
        global current_taskid
        current_taskid = taskid
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
    global current_groupid
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    exists = tasksExists(taskname)
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M")

    assigned = ' '.join(findAssignment(taskname))

    taskid_arr = findTaskID(taskname)
    taskid = ','.join(str(v) for v in taskid_arr)

    subtasks_res = getSubtasks(taskname)
    try:
        subtasks_arr = list(subtasks_res[0])[0]

        mongo_template = { "history_id": int(datetime.now().timestamp()),
        "task_id": int(taskid),
        "group_id": current_groupid,
        "taskname": taskname,
        "username": current_username,
        "date": date,
        "time": time,
        "assignedto": assigned,
        "subtasks": subtasks_arr}
    except:
        mongo_template = { "history_id": int(datetime.now().timestamp()),
        "task_id": int(taskid),
        "group_id": current_groupid,
        "taskname": taskname,
        "username": current_username,
        "date": date,
        "time": time,
        "assignedto": assigned}
  

    if exists:
        exists = 'true' 
        taskname = "'" + taskname + "'"
        username = "'" + current_username + "'"
        status = "'complete'"
        date = "'" + date + "'"
        time = "'" + time + "'"
        a = int(current_groupid)
        query = 'UPDATE tasks_table SET doneby = %s, status = %s, completeddate = %s, completedtime = %s WHERE taskname = %s AND groupid::int = %i;' % (username, status, date, time, taskname, a)
        cursor.execute(query)
        conn.commit()
        mycol.insert_one(mongo_template)
   
    else:
        exists = 'false'
    
    return exists

def countOverallTasks():
    global current_groupid
    final_dict = {}
    users = []
    vals = []

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid}},

    {"$group" :  
        {"_id" : "$username",  
         "num" : {"$sum" : 1} 
         }},
    {"$project" : 
        { "_id": 0, "username": "$_id", "num": 1 } },
    { "$sort" : 
        SON([("num", -1)]) } 
    ]) 

    result = list(agg_result)
    all_users = getUsernames(current_groupid)

    users_arr = []
    for e1 in all_users:
        users_arr.append(" ".join(list(e1)))
    for u in users_arr:
        for d in result:
            if d['username'] == u:
                name = getUser(d['username'])
                user = " ".join(list(name)).title()
                val = d['num']
                final_dict[user] = val
            
                users.append(user)
                vals.append(vals)
    
    
    return final_dict

def countRecurringTasks():
    global current_groupid
    final_dict = {}
    users = []
    vals = []
    vals0 = []
    all_rec_tasks = getRecurringTaskNames()
    tasks_arr = []
    
    for e2 in all_rec_tasks:
        tasks_arr.append(" ".join(list(e2)))

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid}},

    {"$group" :  
        {"_id" : "$username",  
         "num" : {"$sum" : 1},
         "taskname": { "$push": "$taskname" } 
         }},
    {"$project" : 
        { "_id": 0, "username": "$_id", "num": 1, "taskname": 1 } },
    { "$sort" : 
        SON([("num", -1)]) } 
    ]) 

    result = list(agg_result)
    all_users = getUsernames(current_groupid)

    users_arr = []
    for e1 in all_users:
        users_arr.append(" ".join(list(e1)))


    for u in users_arr:
        for d in result:
            if d['username'] == u:
                vals0.append(d['num'])
                for t in d['taskname']:
                    if t not in tasks_arr:
                        d['num'] = d['num'] - 1

                name = getUser(d['username'])
                user = " ".join(list(name)).title()
                val = d['num']
                final_dict[user] = val
            
                users.append(user)
                vals.append(val)
    
    print(final_dict)
    return final_dict


def countIndivTasks():
    global current_groupid
    complete_list = {}
    only_vals = {}
    all_tasks = getRecurringTaskNames()

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid}},

    {"$group" :  
        {"_id" : {"username":"$username", "taskname": "$taskname"},  
         "num" : {"$sum" : 1} 
         }},
    {"$project" : 
        { "_id": 0, "categories": "$_id", "num": 1 } },
    { "$sort" : 
        SON([("username", -1)]) } 
    ]) 
    result = list(agg_result)

    
    all_users = getUsernames(current_groupid)

    users_arr = []
    tasks_arr = []
    for e1 in all_users:
        users_arr.append(" ".join(list(e1)))

    #print(users_arr)

    for e2 in all_tasks:
        tasks_arr.append(" ".join(list(e2)))
    #print(tasks_arr)


    for u in users_arr:
        temp_arr = []
        for t in tasks_arr:
            found = False
            for r in result:
                if r['categories']['username'] == u and r['categories']['taskname'] == t:
                    complete_list[u + '-' + t] = r['num']
                    temp_arr.append(r['num'])
                    found = True
            if not found:
                complete_list[u + '-' + t] = 0
                temp_arr.append(0)

        name = getUser(u)
        user = " ".join(list(name)).title()

        only_vals[user] = temp_arr

    dummy_tasks_dict = {}
    for i in range(0, len(tasks_arr)):
        dummy_tasks_dict['task-' + str(i)] = tasks_arr[i]

    #print(complete_list)
    #print(only_vals)
    #print(dummy_tasks_dict)
    return only_vals, dummy_tasks_dict

def earliestActive():
    global current_groupid
   

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid}},

    {"$group" :  
        {"_id": { "$substr": ["$date", 0, 2 ] },
         }},
    {"$project" : 
        { "_id": 0, "month": "$_id"} },
    { "$sort" : 
        SON([("month", 1)]) },
    { "$limit" :
        1}
    ]) 

    result = list(agg_result)
    try:
        earliest = result[0]['month']
    except:
         now = datetime.now()
         earliest  = now.strftime("%m")
    return earliest


def myTaskCompletions():
    global current_username
    global current_groupid
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    final_dict = {}
    username = str(current_username)

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid, "username":username}},

    {"$group" :  
        {"_id": { "$substr": ["$date", 0, 2 ] },
         "num" : {"$sum" : 1} 
         }},
    {"$project" : 
        { "_id": 0, "month": "$_id", "num": 1 } },
    { "$sort" : 
        SON([("month", 1)]) } 
    ]) 

    result = list(agg_result)

    start = earliestActive()
    now = datetime.now()
    end = now.strftime("%m")
    start = mapMonthNums(start)
    end = mapMonthNums(end)


    for i in range(start, end + 1):
        monthExists = False
        for d in result:
            num = mapMonthNums(d['month'])
            if num == i:
                monthName = mapMonthNames(i)
                month = monthName
                val = d['num']
                final_dict[month] = val
                monthExists = True
        if not monthExists:
            monthName = mapMonthNames(i)
            month = monthName
            val = 0
            final_dict[month] = val
    
    return final_dict

def myTaskMisses():
    global current_username
    global current_groupid
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    final_dict = {}
    username = str(current_username)

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid, "assignedto":username, "username": { "$ne": username }}},

    {"$group" :  
        {"_id": { "$substr": ["$date", 0, 2 ] },
         "num" : {"$sum" : 1} 
         }},
    {"$project" : 
        { "_id": 0, "month": "$_id", "num": 1 } },
    { "$sort" : 
        SON([("month", 1)]) } 
    ]) 

    result = list(agg_result)
    #print(result)

    start = earliestActive()
    now = datetime.now()
    end = now.strftime("%m")
    start = mapMonthNums(start)
    end = mapMonthNums(end)

    
    for i in range(start, end + 1):
        monthExists = False
        for d in result:
            num = mapMonthNums(d['month'])
            if num == i:
                monthName = mapMonthNames(i)
                month = monthName
                val = d['num']
                final_dict[month] = val
                monthExists = True
        if not monthExists:
            monthName = mapMonthNames(i)
            month = monthName
            val = 0
            final_dict[month] = val
    
    return final_dict

def mapMonthNames(num):
    all_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
    6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
    12: 'December'}
   

    return all_months[num] 

def mapMonthNums(month):
    month_nums = {'01': 1, '02': 2, '03': 3, '04': 4, '05': 5,
    '06': 6, '07': 7, '08': 8, '09': 9, '10': 10, '11': 11,
    '12': 12}
   

    return month_nums[month] 

def myTopTasks():
    global current_groupid
    global current_username
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    top_tasks = []
    username = str(current_username)

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid, "username":username}},

    {"$group" :  
        {"_id": "$taskname",
         "num" : {"$sum" : 1} 
         }},
    {"$project" : 
        { "_id": 0, "taskname": "$_id", "num": 1 } },
    {"$sort" : 
        SON([("num", -1)]) },
    ]) 

    result = list(agg_result)

    try:
        maxVal = result[0]['num']
    except: 
        return

    for r in result:
        if r['num'] == maxVal:
            top_tasks.append(r['taskname'])

    if len(top_tasks) == 0:
        top_tasks = 'No Tasks Completed'
    elif len(top_tasks) == 1:
        top_tasks = " ".join(top_tasks)
    else:
        top_tasks = ', '.join(top_tasks)

    return top_tasks

def myBottomTasks():
    global current_groupid
    global current_username
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    final_dict = {}
    bottom_tasks = []
    all_tasks = getRecurringTaskNames()
    tasks_arr = []

    for e2 in all_tasks:
        tasks_arr.append(" ".join(list(e2)))

    username = str(current_username)

    agg_result= mycol.aggregate( 
    [{ 
    "$match":
    {"group_id":current_groupid, "username":username}},

    {"$group" :  
        {"_id": "$taskname",
         "num" : {"$sum" : 1} 
         }},
    {"$project" : 
        { "_id": 0, "taskname": "$_id", "num": 1 } },
    {"$sort" : 
        SON([("num", 1)]) },
    ]) 

    result = list(agg_result)
    #print(result)
    try:
        minVal = result[0]['num']
    except: 
        return
    
    #print(minVal)

    completedAllTasks = True

    for t in tasks_arr:
        found = False
        for r in result:
            if r['taskname'] == t:
                found = True
        if not found:
            bottom_tasks.append(t)
            completedAllTasks = False


    if completedAllTasks == True:
        for r in result:
            if r['num'] == minVal:
                bottom_tasks.append(r['taskname'])
    
    
    if len(bottom_tasks) == 0:
        bottom_tasks = 'No Tasks Completed'
    elif len(bottom_tasks) == 1:
        bottom_tasks = " ".join(bottom_tasks)
    else:
        bottom_tasks = ', '.join(bottom_tasks)
    
    return bottom_tasks

def updateTask(taskname, cursor=cur):
    global current_groupid
    global current_username
    try:
        current_username = db.get('current_username')
        current_groupid = db.get('current_groupid')
    except:
        print("Local")
    exists = tasksExists(taskname)
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    time = now.strftime("%H:%M")

    assigned = ' '.join(findAssignment(taskname))

    taskid = findTaskID(taskname)

    if exists:
        exists = 'true' 
        taskname = "'" + taskname + "'"
        status = "'complete'"
        assignedto = "'" + assignedto + "'"
        a = int(current_groupid)
        query = 'UPDATE tasks_table SET assignedto = %s WHERE taskname = %s AND groupid::int = %i;' % (assignedto, taskname, a)
        cursor.execute(query)
        conn.commit()
        
    else:
        exists = 'false'
    
    return exists

def findSubtasks(word, mysub=mysub):
    # word = "/^" + str(word) + "/"
    global stop_words
    if word in stop_words:
        return []
    word = ".*^" + word + ".*"
    #{ "$regex": /^word/}
    # query = {"keyword": word }, {"_id": 0, "subtask": 1}
    array = []
    subtasks = mysub.find({"keyword":  { "$regex": word, "$options" :'i' }}, {"_id": 0, "subtask": 1})
    for i in subtasks:
        array = i['subtask']
    return array

def findMaterials(word, mysub=mysub):
    global stop_words
    if word in stop_words:
        return []
    word = ".*^" + word + ".*"
    array = []
    materials = mysub.find({"keyword":  { "$regex": word, "$options" :'i' }}, {"_id": 0, "materials": 1})
    for i in materials:
        array = i['materials']
    return array

def convertArray(array):
    array = json.dumps(array)
    array = str(array)
    array = array.replace('[', '{')
    array = array.replace(']', '}')
    array = "'" + array + "'"
    return array

def getArrSubtask(taskname):
    keys = taskname.split()
    subtasks = []
    for word in keys:
        stask = findSubtasks(word)
        subtasks = stask + subtasks

    return subtasks
def getArrMaterials(taskname):
    keys = taskname.split()
    materials = []
    for word in keys:
        mats = findMaterials(word)
        materials = mats + materials
    return materials

def updateSubMat(subtaskarr, materialarr, cursor = cur):
        ## need to insert users adding and subtracting their preferences.
    global current_taskid
    if len(subtaskarr) != 0 or len(materialarr) != 0:
        subtasks = convertArray(subtaskarr)
        materials = convertArray(materialarr)
        #need to reformat subtasks and materiasl from being [] to '{"209-240-9984", "209-256-6897"}' LOL kms
        query = 'UPDATE tasks_table SET subtasks = %s, materials = %s WHERE taskid = %s;' % (subtasks, materials, current_taskid)
        cursor.execute(query)
        conn.commit()
    return 'false'

def getATask(taskname, cursor = cur):
    global current_groupid 
    taskname = "'" + taskname + "'"
    query = "SELECT assignedto, subtasks, materials, notes FROM tasks_table WHERE tasks_table.taskname = %s AND groupid::int = %i;" % (taskname, current_groupid)
    cur.execute(query)
    return cur.fetchall() 

#this is dumb lol
def changeStuff(taskname, assignedto, subtaskarr, materialarr, usernotes, cursor = cur):
    global current_groupid
    subtasks = convertArray([])
    materials = convertArray([])
    if len(subtaskarr) != 0 or len(materialarr) != 0:
        subtasks = convertArray(subtaskarr)
        materials = convertArray(materialarr)
    taskname = "'" + taskname + "'"
    assignedto = "'" + assignedto + "'"
    notes = "'" + usernotes + "'"
    a = int(current_groupid)
    query = "UPDATE tasks_table SET assignedto = %s, subtasks = %s, materials = %s, notes = %s WHERE taskname = %s AND groupid::int = %i;" % (assignedto, subtasks, materials, notes, taskname, a)
    cur.execute(query)
    conn.commit()
    try:
        query = "UPDATE recurring_table SET assignedto = %s, subtasks = %s, materials = %s, notes = %s WHERE taskname = %s AND groupid::int = %i;" % (assignedto, subtasks, materials, notes, taskname, a)
        cur.execute(query)
        conn.commit()
        return True
    except:
        return True

def getCompleted(cursor = cur):
    global current_groupid
    curr_gid = "'" + str(current_groupid) + "'"
    # query = 'SELECT DISTINCT firstname, lastname, users.groupid, cnt FROM((SELECT doneby, count(DISTINCT taskid) as cnt FROM history_table WHERE history_table.groupid = %s AND doneby IS NOT NULL GROUP BY doneby) r JOIN history_table t on r.doneby = t.doneby) NATURAL JOIN users WHERE users.username = t.doneby ORDER BY  firstname;' % current_groupid
    query = 'SELECT DISTINCT firstname, lastname, users.groupid, cnt FROM((SELECT doneby, count(DISTINCT taskid) as cnt FROM history_table WHERE history_table.groupid = %s AND doneby IS NOT NULL GROUP BY doneby) r JOIN history_table t on r.doneby = t.doneby) NATURAL JOIN users WHERE users.username = t.doneby ORDER BY  firstname;' % curr_gid
    cur.execute(query)
    return cur.fetchall()

def getRecurrance(cursor = cur):
    global current_groupid
    a = int(current_groupid)
    query = "SELECT E.taskname, D.repeattime FROM (SELECT taskid, taskname, groupid FROM tasks_table ) E LEFT JOIN (SELECT taskid, taskname, groupid ,repeattime FROM recurring_table) D ON E.taskid = D.taskid WHERE E.groupid::int = %i;" % a
    cur.execute(query)
    return cur.fetchall()

