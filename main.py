

from flask import Flask, request, abort, make_response
from settings import dbpwd
import mysql.connector as mysql
import json
import uuid
import bcrypt

db = mysql.connect(
    host="danielslotin-dbblog.cbrdyb6rueag.eu-central-1.rds.amazonaws.com",
    user="admin",
    password="danielslotin61",
    database="dbblog")

print(db)

app = Flask(__name__)


@app.route('/posts', methods=['GET', 'POST'])
def manage_posts():
    if request.method == 'GET':
        return get_all_posts()
    else:
        return add_post()


def get_all_posts():
    query = "SELECT id, title, body, user_id, comment_id, tag_id, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') AS formatted_created_at, img  from posts"
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    print(records)


    header = ['id','title', 'body','user_id','comment_id','tag_id','created_at','img']
    data = []
    for r in records:
        data.append(dict(zip(header, r)))
    return json.dumps(data)


def get_post(id):
    query = "SELECT id, title, body, comment_id, tag_id, img, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') AS formatted_created_at, user_id from posts where id = %s"
    values = (id,)
    cursor = db.cursor()
    cursor.execute(query, values)
    record = cursor.fetchone()
    cursor.close()
    header = ['id', 'title', 'body', 'comment_id', 'tag_id', 'created_at', 'img', 'user_id']
    return json.dumps(dict(zip(header, record)))


def add_post():
    data = request.get_json()
    print(data)
    query = "INSERT INTO posts ( title, body) VALUES (%s, %s)"
    values = (data['title'], data['body'])


    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    new_post_id = cursor.lastrowid
    cursor.close()
    return get_post(new_post_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    query = "select id, username, password from users where username = %s"
    values = (data['user'],)
    cursor = db.cursor()
    cursor.execute(query, values)
    record = cursor.fetchone()
    cursor.close()

    if not record:
        abort(401)

    user_id = record[0]
    hashed_pwd = record[2].encode('utf-8')

    if bcrypt.hashpw(data['pass'].encode('utf-8'), bcrypt.gensalt()) == hashed_pwd:
        abort(401)

    query = "insert into sessions (user_id, session_id) values (%s, %s) ON DUPLICATE KEY UPDATE session_id = %s"
    session_id = str(uuid.uuid4())
    values = (record[0], session_id, session_id)
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    resp = make_response()
    resp.set_cookie("session_id", session_id)
    return resp

@app.route('/signup', methods=['POST'])
def signup():
        data = request.get_json()
        print(data)
        username = data['username']
        password = data['password']

        # Check if the username already exists in the database
        query = "SELECT id FROM users WHERE username = %s"
        values = (username,)
        cursor = db.cursor()
        cursor.execute(query, values)
        record = cursor.fetchone()
        cursor.close()
        print(data)

        if record:
            abort(409)  # username already exists

        # Hash the password
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the users table
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, hashed_pwd)
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        resp = make_response()
        resp.status_code = 201  # Created
        return "Signup successful!"

def check_login():
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(401)
    query = "select user_id from sessions where session_id = %s"
    values = (session_id,)
    cursor = db.cursor()
    cursor.execute(query, values)
    record = cursor.fetchone()
    cursor.close()
    if not record:
        abort(401)


if __name__ == "__main__":
    app.run()