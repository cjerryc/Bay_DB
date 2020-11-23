import pymongo
import psycopg2

client = pymongo.MongoClient("mongodb+srv://ogencer2:iWMOdvjfmgaKTLmO@cluster0.iez4s.mongodb.net/BayDB?retryWrites=true&w=majority")
db = client.test
print(db)

mydb = client["BayDB"]
mycol = mydb["BayDB"]

conn = psycopg2.connect(
        host="ec2-52-200-134-180.compute-1.amazonaws.com",
        database="d6ehld1vcv1vv1",
        user="vuxncunnoferwp",
        password="bab2d1e1b712cbc8c6a16c50213d0d5888c7b53c74ea961aba4a708f55e36115")
cur = conn.cursor()

def checkGroupID(usrnm, cursor=cur):
    usrnm = "'" + usrnm + "'"
    query = 'Select Groupid FROM groups WHERE %s = ANY (Username);' %usrnm
    cursor.execute(query)
    return (int(cursor.fetchone()[0]))

mongo_template = { "history_id": 5,
          "task_id": 4,
          "group_id": 3,
          "taskname": "LoL",
          "username": "ogencer2",
          "date": "10/12/2020",
          "time": "14:10",
          "was_assigned": True,
          "subtasks": ["hi", "lol", "love"]}

mongo_template1 = { "history_id": 2,
          "task_id": 1,
          "group_id": 3,
          "taskname": "counter clean",
          "username": "ddd2",
          "date": "10/10/2020",
          "time": "17:10",
          "was_assigned": False,
          "subtasks": ["soap", "counter", "clean", "wipe"]}

myquery = { "username": "ogencer2" }
myquery1 = { "history_id": { "$gt": 1 } }

#mycol.insert_one(mongo_template)
#mycol.insert_one(mongo_template1)

mydoc = mycol.find(myquery1)

for x in mydoc:
  print(x)
print((checkGroupID('ogencer2')))