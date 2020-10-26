# app.py
from flask import Flask, request, jsonify, render_template
from connectToDB import getUser
app = Flask(__name__)


# A welcome message to test our server
@app.route('/index')
@app.route('/')
def index():
    return "<h1>Welcome to our CS411 Project Website !!</h1> <p>by Ozgur Gencer and Ryohei Namiki</p>"


@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    try:
        results = getUser(username)
        return render_template('welcome.html', name=results[0], lastname=results[1])
    except:
        return render_template('welcome.html', name=None, lastname=None)



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)