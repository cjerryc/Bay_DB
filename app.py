# app.py
from flask import Flask, request, jsonify, render_template
from connectToDB import getUser, logUserIn, createUser
app = Flask(__name__)


@app.route('/index')
@app.route('/')
def index():
    return "<h1>Welcome to our CS411 Project Website !!</h1> <p>by Ozgur Gencer, Veda Menon, Lucy Zhang, Jerry Chang</p>"


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
        if queryRes:
            return render_template('welcome.html', name=queryRes[0], lastname=queryRes[1])
        else:
            return "<h1>Username or Password is wrong!!</h1> <p>try again!</p>"

    


@app.route('/signinfo', methods = ['POST', 'GET'])
def signinfo():
   if request.method == 'POST':
      result = request.form
      #print(result)
      createUser(result["username"], result["firstname"], result["lastname"], result["email"], result["passcode"])
      #print(result["username"])
      return render_template("signupinfo.html", result = result)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)