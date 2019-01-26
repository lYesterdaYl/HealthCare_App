from flask import Flask, request, jsonify, make_response, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Walk_Data, Calories_Data, Survey_Data

import json
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

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/create_account', methods=['POST'])
def create_account():
    """

    :return:
    """
    response = {}
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        gender = request.form.get("gender", "0")
        age = request.form.get("age", "")
        telephone = request.form.get("telephone", "")
        country = request.form.get("country", "")
        state = request.form.get("state", "")
        city = request.form.get("city", "")

        if username == "" or password == "":
            response['msg'] = "Username or Password is empty"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)

        # md5 encryption
        encryption = hashlib.md5()
        encryption.update(password.encode(encoding='utf-8'))
        password = encryption.hexdigest()

        user = session.query(User).filter_by(username=username).first()
        if user is None:
            new_user = User(username=username, password=password, gender=gender, age=age,
                            telephone=telephone, country=country, state=state, city=city)
            session.add(new_user)
            session.commit()
            response['msg'] = "User Created"
            response['code'] = "200"
            return  make_response(json.dumps(response), 200)
        else:
            response['msg'] = "User Already Exist"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)

    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "200"
        return make_response(json.dumps(response), 405)


@app.route('/user/login', methods=['POST'])
def user_login():
    """
    App login function
    :return: {"msg": "auth successful", "data": "", "code": "200"}
    """

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

            data = {}
            data['id'] = user.id
            data['username'] = user.username
            data['gender'] = user.gender
            data['age'] = user.age
            data['telephone'] = user.telephone
            data['country'] = user.country
            data['state'] = user.state
            data['city'] = user.city
            data['country'] = user.country
            data['session'] = user.session

            response['msg'] = "Auth successful"
            response['data'] = data
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "Wrong username or password"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)


@app.route('/data/<int:user_id>/JSON', methods=['POST'])
def get_user_data(user_id):
    response = {}
    if request.method == 'POST':
        user = session.query(User).filter_by(id=user_id).first()
        if user.session == request.form['session']:
            if 'data_type' in request.form:
                if 'start_date' in request.form and 'end_date' in request.form:
                    start_date, end_date = request.form['start_date'], request.form['end_date']
                    if request.form['data_type'] == 'walk':
                        data = session.query(Walk_Data).filter_by(user_id=user_id)\
                            .filter(Walk_Data.date>=start_date, Walk_Data.date<=end_date)
                    elif request.form['data_type'] == 'calorie':
                        data = session.query(Calories_Data).filter_by(user_id=user_id)\
                            .filter(Calories_Data.date>=start_date, Calories_Data.date<=end_date)
                    else:
                        data = {}
                        response['msg'] = "No Data on such Dates"
                        response['data'] = data
                        response['code'] = "200"
                        return make_response(json.dumps(response), 200)
                    response['msg'] = "Data Retrive Successful"
                    response['data'] = data
                    response['code'] = "200"
                    return make_response(json.dumps(response), 200)
                else:
                    response['msg'] = "Start Date or End Date is Empty"
                    response['code'] = "200"
                    return make_response(json.dumps(response), 200)
            else:
                response['msg'] = "Request Data Type is Empty"
                response['code'] = "200"
                return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "Please Login or Re-Login"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)


@app.route('/user/<int:user_id>/update', methods=['POST'])
def update_user_information(user_id):
    response = {}
    if request.method == 'POST':
        user = session.query(User).filter_by(id=user_id).first()
        if user.session == request.form['session']:
            user.gender = request.form.get("gender", user.gender)
            user.age = request.form.get("age", user.age)
            user.telephone = request.form.get("telephone", user.telephone)
            user.country = request.form.get("country", user.country)
            user.state = request.form.get("state", user.state)
            user.city = request.form.get("city", user.city)

            session.add(user)
            session.commit()

            response['msg'] = "User Information Edit Successful"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "Please Login or Re-Login"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)


@app.route('/data/<int:user_id>/insert', methods=['POST'])
def insert_user_data(user_id):
    response = {}
    if request.method == 'POST':
        user = session.query(User).filter_by(id=user_id).first()
        if user.session == request.form['session']:
            if 'data_type' in request.form:
                data = json.loads(request.form['data'])
                if request.form['data_type'] == 'walk':
                    new_data = Walk_Data(walk=data['walk'], date=data['date'], user_id=user_id)
                elif request.form['data_type'] == 'calorie':
                    new_data = Calories_Data(calorie=data['walk'], date=data['date'], user_id=user_id)
                elif request.form['data_type'] == 'survey':
                    score = data['Q1'] + data['Q2'] + data['Q3'] + data['Q4'] + data['Q5'] \
                            + data['Q6'] + data['Q7'] + data['Q8'] + data['Q9'] + data['Q10']
                    new_data =  Survey_Data(Q1=data['Q1'], Q2=data['Q2'], Q3=data['Q3'], Q4=data['Q4'], Q5=data['Q5'],
                                            Q6=data['Q6'], Q7=data['Q7'], Q8=data['Q8'], Q9=data['Q9'], Q10=data['Q10'],
                                            score=score, date=data['date'])
                else:
                    response['msg'] = "Please Invalid Data Type"
                    response['code'] = "200"
                    return make_response(json.dumps(response), 200)
                session.add(new_data)
                session.commit()
            else:
                response['msg'] = "Please Specify Data Type"
                response['code'] = "200"
                return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "Please Login or Re-Login"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)


if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(port=5000)
