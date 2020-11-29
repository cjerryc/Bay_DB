# app.py
from flask import Flask, request, jsonify, render_template
from connectToDB import getUser, logUserIn, logUserOut, createUser, getUserInfo, createTask, getTasks, getGroupMembers, searchTasks, updateTask, deleteTask, completeTask, getGroupName, countOverallTasks, countIndivTasks, myTaskCompletions, myTaskMisses, myTopTasks, myBottomTasks, joinGroup, leaveGroup, createGroup
app = Flask(__name__)
current_firstname = "''"
current_lastname = "''"


@app.route('/')
def index():
    return render_template('login.html', wrongPass = False)


@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    try:
        results = getUser(username)
        return render_template('welcome.html', name=results[0])
    except:
        return render_template('welcome.html', name=None, lastname=None)

@app.route('/login')
def login():
    print('LOGOUT')
    logUserOut()
    return render_template('login.html', wrongPass = False)

@app.route('/managelogin', methods = ['POST', 'GET'])
def managelogin():
    if request.method == 'POST':
        result = request.form
        try:
            queryRes = logUserIn(result["username"], result["passcode"])
            current_firstname = queryRes[0]
            current_lastname = queryRes[1]
            tasks = getTasks()
            #if queryRes:
                #return render_template('home.html', name=queryRes[0], lastname=queryRes[1])
            if queryRes:
                return render_template('home.html', tasks = getTasks())

            else:
                return "<h1>Username or Password is wrong!!</h1> <p>try again!</p>"
        except:
            return render_template('login.html', wrongPass = True)

@app.route('/group',  methods = ['POST', 'GET'])
def groupinfo():
    userinfo = getUserInfo()
    try:
        groupid = userinfo[5]
        print(groupid)
        groupname = getGroupName(groupid)
        print(groupname[0][0])
        groupmembers = getGroupMembers(groupid)
        return render_template('group.html', groupid = groupid, groupname = groupname[0][0], groupmembers = groupmembers)
    except:
        return render_template('createjoingroup.html') ##this mean the person doesn have a group

@app.route('/groupjoined',  methods = ['POST', 'GET'])
def groupjoined():
    result = request.form
    joinGroup(result['groupid'])
    userinfo = getUserInfo()
    try:
        groupid = userinfo[5]
        print(groupid)
        groupname = getGroupName(groupid)
        print(groupname[0][0])
        groupmembers = getGroupMembers(groupid)
        return render_template('group.html', groupid = groupid, groupname = groupname[0][0], groupmembers = groupmembers)
    except:
        return render_template('createjoingroup.html') ##this mean the person doesn have a group

@app.route('/createdGroup',  methods = ['POST', 'GET'])
def createdGroup():
    result = request.form
    createGroup(result['groupname'], result['groupid'])
    userinfo = getUserInfo()
    try:
        groupid = userinfo[5]
        print(groupid)
        groupname = getGroupName(groupid)
        print(groupname[0][0])
        groupmembers = getGroupMembers(groupid)
        return render_template('group.html', groupid = groupid, groupname = groupname[0][0], groupmembers = groupmembers)
    except:
        return render_template('createjoingroup.html') ##this mean the person doesn have a group

@app.route('/home')
def home():
    tasks = getTasks()
    return render_template('home.html', tasks = getTasks())

@app.route('/dashboard')
def dashboard():
    ret_c1 = countOverallTasks()
    ret_c2, tasks_c2 = countIndivTasks()

    try:
        keys_c1, vals_c1 = zip(*ret_c1.items())
        user_keys_c2, vals_c2 = zip(*ret_c2.items())
        dummy_vals, tasks_keys_c2 = zip(*tasks_c2.items())
        print(tasks_keys_c2)
        return render_template('dashboard.html', key_c1 = keys_c1, val_c1 = vals_c1, task_keys_c2 = tasks_keys_c2, val_c2 = vals_c2 )
        #k = jsonify({'key_list': keys_c1})
        #v = jsonify({'val_list': vals_c1})
    except:
        return "<h1>No Data Available</h1>"

@app.route('/progress')
def progress():
    ret_c1 = myTaskCompletions()
    ret_c3, tasks_c3 = countIndivTasks()
    top_tasks = myTopTasks()
    bottom_tasks = myBottomTasks()
    ret_c2 = myTaskMisses()

    try:
        keys_c1, vals_c1 = zip(*ret_c1.items())
        keys_c2, vals_c2 = zip(*ret_c2.items())
        user_keys_c3, vals_c3 = zip(*ret_c3.items())
        dummy_vals, tasks_keys_c3 = zip(*tasks_c3.items())
        return render_template('progress.html', top_tasks = top_tasks, bottom_tasks = bottom_tasks, key_c1 = keys_c1, val_c1 = vals_c1, key_c2 = keys_c2, val_c2 = vals_c2, task_keys_c3 = tasks_keys_c3, val_c3 = vals_c3 )

    except:
         return "<h1>No Data Available</h1>"

@app.route('/data')
def data():
    ret = countTasks()
    #counts = jsonify({'results': ret['values']})
    keys, vals = zip(*ret.items())
   
    k = jsonify({'key_list': keys})
    v = jsonify({'val_list': vals})
    print(keys)
    print(vals)
    return v

@app.route('/updatetask', methods = ['POST', 'GET'])
def updateTask():
    return render_template('updatetask.html', tasks = getTasks())

@app.route('/deletetask', methods = ['POST', 'GET'])
def deletetask():
    if request.method == 'POST':
        result = request.form
        try:
            do = deleteTask(result['taskname'])
            return render_template("taskdeleted.html", taskname=result["taskname"], exists=do, tasks = getTasks())
        except:
            exists = False
            return render_template("taskdeleted.html", taskname=result["taskname"], tasks = getTasks())
        # if do:
        #     return render_template("taskdeleted.html", taskname=result["taskname"], exists=do)
    return render_template('deletetask.html', tasks = getTasks())

@app.route('/completetask', methods = ['POST', 'GET'])
def completetask():
    if request.method == 'POST':
        result = request.form
        
        try:
            exists = completeTask(result["taskname"])
            return render_template("taskcompleted.html", taskname=result["taskname"], exists=exists, tasks = getTasks())
        except Exception as inst:
            print(inst)
            return "<h1>Error try again!</h1>"
    return render_template('completetask.html', tasks = getTasks())

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        result = request.form
        queryRes = searchTasks(result["search"])
        if queryRes and result["search"] :
            return render_template('search.html', searchInput = "Search results for '" + result["search"] + "'", searchedTasks=queryRes, tasks = getTasks())
        elif not result["search"]:
            return render_template('search.html', searchInput = "No results could be found!", searchedTasks= '', tasks = getTasks())
        else:
            return render_template('search.html', searchInput = "No results for '" + result["search"] + "' could be found!", searchedTasks= '', tasks = getTasks())
    elif request.method == 'GET':
        return render_template('search.html', tasks = getTasks())
    return render_template('search.html', tasks = getTasks())
    
@app.route('/addtask', methods = ['POST', 'GET'])
def addtask():
    if request.method == 'POST':
        result = request.form
        # print(result)
        exists = createTask(result["taskname"], result["assignedto"], result["repeat"], result["usernotes"])
        ##this is for cdc stuff:
        if 'CDCoption' in result.keys():
            ##do mongo stuff 
            print("insertmongostuff")
        # print(exists)
        return render_template('taskcreated.html', taskname=result["taskname"], exists=exists, tasks = getTasks())
    return render_template('addtask.html', tasks = getTasks())     


@app.route('/signinfo', methods = ['POST', 'GET'])
def signinfo():
   if request.method == 'POST':
      result = request.form
      #print(result)

      try:
        createUser(result["username"], result["firstname"], result["lastname"], result["email"], result["passcode"])
        #print(result["username"])
        return render_template("profile.html", result = result)
      except:
          return "<h1>Password doesn't match try again!</h1>"

@app.route('/profile')
def profilepage():
    result = getUserInfo()
    return render_template('profile.html', result = result)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)