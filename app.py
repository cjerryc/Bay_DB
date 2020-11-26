# app.py
from flask import Flask, request, jsonify, render_template
from connectToDB import getUser, logUserIn, logUserOut, createUser, createTask, getTasks, searchTasks, updateTask, deleteTask, completeTask
app = Flask(__name__)
current_firstname = "''"
current_lastname = "''"


@app.route('/')
def index():
    #return render_template('index.html') #change to 'login.html' later
    return render_template('login.html')


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
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/managelogin', methods = ['POST', 'GET'])
def managelogin():
    if request.method == 'POST':
        result = request.form
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

@app.route('/home')
def home():
    tasks = getTasks()
    return render_template('home.html', tasks = getTasks())
    
@app.route('/addtask')
def addtask():
    tasks = getTasks()
    return render_template('addtask.html', tasks = getTasks())

@app.route('/completetask')
def completetask():
    return render_template('completetask.html', tasks = getTasks())

@app.route('/deletetask', methods = ['POST', 'GET'])
def deletetask():
    if request.method == 'POST':
        result = request.form
        print(result)
        try:
            do = deleteTask(result['taskname'])
            return render_template("taskdeleted.html", taskname=result["taskname"], exists=do, tasks = getTasks())
        except:
            exists = False
            return render_template("taskdeleted.html", taskname=result["taskname"], tasks = getTasks())
        # if do:
        #     return render_template("taskdeleted.html", taskname=result["taskname"], exists=do)
    return render_template('deletetask.html', tasks = getTasks())

@app.route('/taskcompleted', methods = ['POST', 'GET'])
def taskcompleted():
    if request.method == 'POST':
        result = request.form
        
        try:
            exists = completeTask(result["taskname"])
            return render_template("taskcompleted.html", taskname=result["taskname"], exists=exists, tasks = getTasks())
        except Exception as inst:
            print(inst)
            return "<h1>Error try again!</h1>"

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        result = request.form
        queryRes = searchTasks(result["search"])
        if queryRes and result["search"] :
            return render_template('search.html', searchInput = "Search results for '" + result["search"] + "'", searchedTasks=queryRes)
        elif not result["search"]:
            return render_template('search.html', searchInput = "No results could be found!", searchedTasks= '')
        else:
            return render_template('search.html', searchInput = "No results for '" + result["search"] + "' could be found!", searchedTasks= '')
    elif request.method == 'GET':
        return render_template('search.html')
    return render_template('search.html')
    
@app.route('/taskcreated', methods = ['POST', 'GET'])
def taskcreated():
    if request.method == 'POST':
        result = request.form
        print(result)
        exists = createTask(result["taskname"], result["assignedto"])
        print(exists)
        return render_template('taskcreated.html', taskname=result["taskname"], exists=exists, tasks = getTasks())     


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

#how do we know who is currently "logged in"? pls fix profile
# @app.route('/profile')
# def profilepage():
#     result = getUserInfo()
#     return render_template('signupinfo.html', result = getUserInfo())


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)