from flask import Flask, request, jsonify, make_response, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User

import json
import requests
import hashlib
import time, random

app = Flask(__name__)

# MySQL database information
DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = ""
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "healthcare_app"
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8"\
    .format(DIALCT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
engine = create_engine(DB_URI)
# engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/create_account', methods=['POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        gender = request.form.get("gender", "")
        age = request.form.get("age", "")
        telephone = request.form.get("telephone", "")
        country = request.form.get("country", "")
        state = request.form.get("state", "")
        city = request.form.get("city", "")

        if username == "" or password == "":
            return make_response("Username or Password is empty", 200)

        # md5 encryption
        encryption = hashlib.md5()
        encryption.update(password.encode(encoding='utf-8'))
        password = encryption.hexdigest()

        user = session.query(User).filter_by(username=username).first()
        if user is None:
            new_user = User(username=username, password=password, gender=gender, age=age, telephone=telephone, country=country, state=state, city=city)
            session.add(new_user)
            session.commit()
            return  make_response('User Created', 200)
        else:
            return make_response('User Already Exist', 200)

    else:
        return make_response('Method Not Allowed', 405)

@app.route('/login', methods=['POST'])
def user_login():
    response = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()

        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        if hash.hexdigest() == user.password:
            now = int(time.time())
            session_code = str(now) + str(random.randint(10000, 99999))

            user.session = session_code
            session.add(user)
            session.commit()
            print(len(session_code))

            response['msg'] = "auth successful"
            response['code'] = "200"
            response['session'] = session_code
            return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "wrong username or password"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)

# @app.route('/<int:user_id>/data/JSON')
# def get_user_data(user_id):
#     test = {}
#     test['account'] = 'fdafa'
#     test['password'] = 'afdfafw'
#     print(user_id)
#     return make_response(json.dumps(test), 200)



if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.run(debug=True, port=5000)
