import os
import psycopg2

#DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except:
    conn = None
cur = conn.cursor()

def getUser(username, cursor=cur):
    username = "'" + username + "'"
    query = 'SELECT firstname, lastname, email FROM users WHERE users.username = %s;' % username
    print(query)
    cur.execute(query)
    return cur.fetchone()
