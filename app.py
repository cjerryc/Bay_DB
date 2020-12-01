# app.py
from flask import Flask, request, jsonify, render_template
from connectToDB import getUser, checkGroupID, getATask, changeStuff, tasksExists, updateSubMat, getArrSubtask, getArrMaterials, logUserIn, logUserOut, createUser, getUserInfo, createTask, getTasks, getGroupMembers, searchTasks, searchHistory, deleteTask, completeTask, getGroupName, countOverallTasks, countIndivTasks, myTaskCompletions, myTaskMisses, myTopTasks, myBottomTasks, joinGroup, leaveGroup, createGroup, getCompleted
app = Flask(__name__)
current_firstname = "''"
current_lastname = "''"
current_taskname = "''"


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
            userinfo = getUserInfo()
            groupid = userinfo[5]
            if queryRes and groupid is not None:
                return home()
            elif queryRes and groupid is None:
                return render_template('createjoingroup.html')
            else:
                return "<h1>Username or Password is wrong!!</h1> <p>try again!</p>"
        except Exception as e:
            return e
            #return render_template('login.html', wrongPass = True)
'''
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
'''
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

@app.route('/exitGroup',  methods = ['POST', 'GET'])
def exitGroup():
    leaveGroup()
    userinfo = getUserInfo()
    try:
        groupid = userinfo[5]
        print(groupid)
        groupname = getGroupName(groupid)
        print(groupname[0][0])
        groupmembers = getGroupMembers(groupid)
        print("groupmemebers: \n")
        print(groupmembers)
        return render_template('group.html', groupid = groupid, groupname = groupname[0][0], groupmembers = groupmembers)
    except:
        return render_template('createjoingroup.html') ##this mean the person doesn have a group

@app.route('/home')
def home():
    
    tasks = getTasks()
    userinfo = getUserInfo()
    print(tasks)
    for item in tasks:
        # item[12] = str(item[12])
        print (type(item[12]))
    return render_template('home.html', tasks = getTasks())
    # try:
    #     groupid = checkGroupID(user)
    #     print(groupid)
    #     return render_template('home.html', tasks = getTasks())
    # except:
    #     return render_template('createjoingroup.html')

@app.route('/group')
def dashboard():
    ret_c1 = countOverallTasks()
    ret_c2, tasks_c2 = countIndivTasks()
    userinfo = getUserInfo()
    exists = "true"
    try:
        groupid = userinfo[5]
        print(groupid)
        groupname = getGroupName(groupid)
        print(groupname[0][0])
        groupmembers = getGroupMembers(groupid)

        try:
            keys_c1, vals_c1 = zip(*ret_c1.items())
            user_keys_c2, vals_c2 = zip(*ret_c2.items())
            dummy_vals, tasks_keys_c2 = zip(*tasks_c2.items())
            print(tasks_keys_c2)
            return render_template('dashboard.html', exists = exists, groupid = groupid, groupname = groupname[0][0], groupmembers = groupmembers, key_c1 = keys_c1, val_c1 = vals_c1, task_keys_c2 = tasks_keys_c2, val_c2 = vals_c2 )
            #k = jsonify({'key_list': keys_c1})
            #v = jsonify({'val_list': vals_c1})
        except:
            exists = "false"
            return render_template('dashboard.html', exists = exists, groupid = groupid, groupname = groupname[0][0], groupmembers = groupmembers, key_c1 = keys_c1, val_c1 = vals_c1, task_keys_c2 = tasks_keys_c2, val_c2 = vals_c2 )
    except:
        return render_template('createjoingroup.html') ##this mean the person doesn have a group

@app.route('/progress')
def progress():
    ret_c1 = ''
    ret_c2 = ''
    ret_c3 = ''
    top_tasks = ''
    bottom_tasks = ''
    
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
def updateTaskPage():
    if request.method == 'POST':
        result = request.form
        exists = tasksExists(result['taskname'])
        print(exists)
        if exists:
            updatableStuff = getATask(result['taskname']) #assignedto, subtasks, materials, notes
            print(updatableStuff)
            subarr = getArrSubtask(result["taskname"])
            matarr = getArrMaterials(result["taskname"])
            #    for x in updatableStuff[0][1]:
            #TypeError: 'NoneType' object is not iterable
            # [('vedanta2', None, None, ' ')]
            if updatableStuff[0][1] != None:
                for x in updatableStuff[0][1]:
                    if x in subarr:
                        subarr.remove(x)
            if updatableStuff[0][2] != None:
                for x in updatableStuff[0][2]:
                    if x in subarr:
                        matarr.remove(x)
            return render_template('updatetaskbody.html', tasks = getTasks(), currtask = result['taskname'], assignedto = updatableStuff[0][0], subtasks = updatableStuff[0][1], othersubtasks = subarr, othermats = matarr , materials = updatableStuff[0][2], notes = updatableStuff[0][3])
        else:
            return render_template('noupdatetask.html', tasks = getTasks())
    return render_template('updatetask.html', tasks = getTasks())

@app.route('/recieveupdatetask', methods = ['POST', 'GET'])
def updateTask():
    assignedto = ""
    subtask = []
    material = []
    if request.method == 'POST':
        result = request.form
        for list_type in request.form.keys():
            if list_type == "taskname":
                taskname = result["taskname"]
            if list_type == "assignedto":
                assignedto = result["assignedto"]
            if list_type == "subtask":
                subtask = request.form.getlist(list_type)
            if list_type == "material":
                material = request.form.getlist(list_type)
            if list_type == "usernotes":
                notes = result["usernotes"]
        exists = changeStuff(taskname, assignedto, subtask, material, notes)
        if len(subtask) == 0:
            subtask = 'false'
        if len(material) == 0:
            material = 'false'
        return render_template('successupdatetask.html', tasks = getTasks(), currtask = taskname, assignedto = assignedto, subtasks = subtask, materials = material, usernotes = notes)


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
        queryRes = searchHistory(result["search"])
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
        print(exists)
        if 'CDCoption' in result.keys() and exists == 'false':
            ##do mongo stuff
            print("insertmongostuff")
            print(result["taskname"])
            subarr = getArrSubtask(result["taskname"])
            matarr = getArrMaterials(result["taskname"])
            if len(subarr) == 0 and len(matarr) == 0:
                return render_template('nosubtaskcreated.html', taskname=result["taskname"], exists=exists, tasks = getTasks())
            global current_taskname 
            current_taskname = result["taskname"]
            return render_template('addsubmat.html', currtask = result["taskname"], tasks = getTasks(), subtasks = subarr, materials= matarr)
        return render_template('taskcreated.html', taskname=result["taskname"], exists=exists, tasks = getTasks())
    return render_template('addtask.html', tasks = getTasks())    
 
@app.route('/addsubtask', methods = ['POST', 'GET'])
def addsubtask():
    global current_taskname 
    if request.method == 'POST':
        result = request.form
        for list_type in request.form.keys():
            if list_type == "subtask":
                subtask = request.form.getlist(list_type)
            if list_type == "material":
                material = request.form.getlist(list_type)
        exists = updateSubMat(subtask, material)
        return render_template('taskcreated.html', taskname= current_taskname, exists=exists, tasks = getTasks())
        
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
    userinfo = getUserInfo()
    groupid = "N/A"
    groupname = "N/A"
    try: 
        groupid = userinfo[5]
        groupname = getGroupName(groupid)
        return render_template('profile.html', result = userinfo, groupid = groupid, groupname = groupname[0][0])
    except:
        return render_template('profile_nogroup.html', result = userinfo, groupid = groupid, groupname = groupname)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)

@app.route('/nameByTask', methods = ['POST', 'GET'])
def nameByTask():
    if request.method == 'POST':
        queryRes = getCompleted()
        for i in range(0, len(queryRes)):
            print(queryRes[i])
            print("\n")
    #     if queryRes:
    #         return render_template('search.html', searchInput = "Search results for '" + result["search"] + "'", searchedTasks=queryRes, tasks = getTasks())
    #  elif request.method == 'GET':
    #     return render_template('search.html', tasks = getTasks())
    # return render_template('search.html', tasks = getTasks())