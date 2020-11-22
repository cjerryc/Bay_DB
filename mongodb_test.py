import pymongo

client = pymongo.MongoClient("mongodb+srv://ogencer2:iWMOdvjfmgaKTLmO@cluster0.iez4s.mongodb.net/BayDB?retryWrites=true&w=majority")
db = client.test
print(db)

mydb = client["BayDB"]
mycol = mydb["BayDB"]


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