# app.py
from flask import Flask, request, jsonify, render_template
from connectToDB import getUser, logUserIn, createUser, createTask, getTasks, searchTasks, updateTask, deleteTask
app = Flask(__name__)
current_firstname = "''"
current_lastname = "''"


@app.route('/')
def index():
    return render_template('index.html')


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
        if queryRes:
            return render_template('welcome.html', name=queryRes[0], lastname=queryRes[1])
        else:
            return "<h1>Username or Password is wrong!!</h1> <p>try again!</p>"

@app.route('/home')
def home():
    tasks = getTasks()
    return render_template('home.html', tasks = getTasks())
    
@app.route('/addtask')
def addtask():
    return render_template('addtask.html')

@app.route('/completetask')
def completetask():
    return render_template('completetask.html')

@app.route('/deletetask', methods = ['POST', 'GET'])
def deletetask():
    if request.method == 'POST':
        result = request.form
        print(result)
        try:
            do = deleteTask(result['taskname'])
            return render_template("taskdeleted.html", taskname=result["taskname"], exists=do)
        except:
            exists = False
            return render_template("taskdeleted.html", taskname=result["taskname"], exists=do)
        # if do:
        #     return render_template("taskdeleted.html", taskname=result["taskname"], exists=do)
    return render_template('deletetask.html')

@app.route('/taskupdated', methods = ['POST', 'GET'])
def taskupdated():
    if request.method == 'POST':
        result = request.form
        
        try:
            exists = updateTask(result["taskname"], result["username"], result["date"], result["time"])
            return render_template("taskupdated.html", taskname=result["taskname"], exists=exists)
        except Exception as inst:
            print(inst)
            return "<h1>Error try again!</h1>"

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        result = request.form
        queryRes = searchTasks(result["search"])
        print(type(queryRes))
        if result["search"] != '':
            return render_template('search.html', searchedTasks=queryRes)
        else:
            missing = "No Tasks Found!"
            return render_template('search.html', searchedTasks=missing)
    elif request.method == 'GET':
        return render_template('search.html')
    return render_template('search.html')
    
@app.route('/taskcreated', methods = ['POST', 'GET'])
def taskcreated():
    if request.method == 'POST':
        result = request.form
        print(result)
        exists = createTask(result["taskname"], result["username"])
        print(exists)
        return render_template('taskcreated.html', taskname=result["taskname"], exists=exists)     


@app.route('/signinfo', methods = ['POST', 'GET'])
def signinfo():
   if request.method == 'POST':
      result = request.form
      #print(result)

      try:
        createUser(result["username"], result["firstname"], result["lastname"], result["email"], result["passcode"])
        #print(result["username"])
        return render_template("signupinfo.html", result = result)
      except:
          return "<h1>Password doesn't match try again!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)