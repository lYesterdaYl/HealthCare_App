from flask import Flask, request, jsonify, make_response, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Walk_Data, Calories_Data, Survey_Data, Music_Data, Video_Data, Music, Video

import json
import hashlib
import time, random

app = Flask(__name__)

# MySQL database information
DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "root"
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
    s = ""
    s += "Available API Address<br>"
    for rule in app.url_map.iter_rules():
        print(type(rule))
        s += str(rule) + "<br>"

    return s


@app.route('/user/create_account', methods=['POST'])
def create_account():
    """
    Create account for users
    :param username: user name
    :param password: user password
    :param gender: user gender(0 for unknown, 1 for male, 2 for female)
    :param age: user age
    :param telephone: user telephone number
    :param country: user country
    :param state: user state
    :param city: user city
    :return:{"msg": "", "code": "200"}
    """
    response = {}
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        gender = request.form.get("gender", "0")
        age = request.form.get("age", 0)
        major = request.form.get("major", "")
        prefer = request.form.get("prefer", "")
        weight = request.form.get("weight", 0)
        target_weight = request.form.get("target_weight", 0)
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
            new_user = User(username=username, password=password, gender=gender, age=age, major=major, prefer=prefer,
                            weight=weight, target_weight=target_weight, telephone=telephone, country=country,
                            state=state, city=city)
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
    :param username: user name
    :param password: user password
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
            data['major'] = user.major
            data['prefer'] = user.prefer
            data['weight'] = user.weight
            data['target_weight'] = user.target_weight
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

@app.route('/user/change_password', methods=['POST'])
def user_change_password():
    """
    allow user to change their password.
    :param username: store user name
    :param password: store user old password
    :param new_password: store user new password
    :return: {"msg": "", "code": "200"}
    """
    response = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        if password == new_password:
            response['msg'] = "Please Choose a Different Password"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        user = session.query(User).filter_by(username=username).first()

        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        if hash.hexdigest() == user.password:
            if password == new_password:
                response['msg'] = "Please Choose a Different Password"
                response['code'] = "200"
                return make_response(json.dumps(response), 200)
            else:
                new_hash = hashlib.md5()
                new_hash.update(new_password.encode(encoding='utf-8'))
                user.password = new_hash.hexdigest()
                session.add(user)
                session.commit()

                response['msg'] = "Change Password Successful"
                response['code'] = "200"
                return make_response(json.dumps(response), 200)
        else:
            response['msg'] = "Wrong Username or Original Password"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
    else:
        response['msg'] = "Method Not Allowed"
        response['code'] = "405"
        return make_response(json.dumps(response), 405)


@app.route('/data/<int:user_id>/JSON', methods=['POST'])
def get_user_data(user_id):
    """
    Get user data for a specific time period and type
    :param user_id: user id
    :param session: session string that acquire from login api
    :param start_date: request user data starting date
    :param end_date: request user data ending date
    :param data_type: "walk" for walk data, "calorie" for calorie data, "survey" for survey data
    :return:
    """
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
                    elif request.form['data_type'] == 'survey':
                        data = session.query(Survey_Data).filter_by(user_id=user_id)\
                            .filter(Survey_Data.date >= start_date, Survey_Data.date <= end_date)
                    elif request.form['data_type'] == 'music':
                        data = session.query(Music_Data).filter_by(user_id=user_id)\
                            .filter(Survey_Data.date >= start_date, Survey_Data.date <= end_date)
                    elif request.form['data_type'] == 'video':
                        data = session.query(Video_Data).filter_by(user_id=user_id)\
                            .filter(Survey_Data.date >= start_date, Survey_Data.date <= end_date)
                    else:
                        data = {}
                        response['msg'] = "No Data on such Dates"
                        response['data'] = data
                        response['code'] = "200"
                        return make_response(json.dumps(response), 200)
                    response['msg'] = "User Information " + str(request.form['data_type']).capitalize() \
                                      +" Data Insert Successful"
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
    """
    Update user information.
    :param user_id: user id
    :param session: session string that acquire from login api
    :param gender: user gender(0 for unknown, 1 for male, 2 for female)
    :param age: user age
    :param telephone: user telephone number
    :param country: user country
    :param state: user state
    :param city: user city
    :return:
    """
    response = {}
    if request.method == 'POST':
        user = session.query(User).filter_by(id=user_id).first()
        if user.session == request.form['session']:
            user.gender = request.form.get("gender", user.gender)
            user.age = request.form.get("age", user.age)
            user.major = request.form.get("major", user.major)
            user.prefer = request.form.get("prefer", user.prefer)
            user.weight = request.form.get("age", user.weight)
            user.target_weight = request.form.get("age", user.target_weight)
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
    """
    Insert user data for a specific type
    :param user_id: user id
    :param session: session string that acquire from login api
    :param data: a json format to store insert data
    :param data_type: "walk" for walk data, "calorie" for calorie data, "survey" for survey data
    :return:
    """
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
                    new_data =  Survey_Data(score=data['score'], date=data['date'], user_id=data['user_id'])
                elif request.form['data_type'] == 'music':
                    new_data =  Music_Data(score=data['score'], date=data['date'], music_id=data['music_id'], user_id=data['user_id'])
                elif request.form['data_type'] == 'video':
                    new_data =  Video_Data(score=data['score'], date=data['date'], video_id=data['video_id'], user_id=data['user_id'])
                else:
                    response['msg'] = "Please Invalid Data Type"
                    response['code'] = "200"
                    return make_response(json.dumps(response), 200)
                session.add(new_data)
                session.commit()
                response['msg'] = "User Information " + str(request.form['data_type']).capitalize() +" Data Insert Successful"
                response['code'] = "200"
                return make_response(json.dumps(response), 200)
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

@app.route('/test', methods=['GET'])
def test():
    n = 0
    m = 0
    for i in range(1,100000):
        if i % 100 == 0:
            n += 1
        music = Music(title=str(i), link=str(i),category=n)
        session.add(music)
    session.commit()

    for i in range(1, 100000):
        if i % 200 == 0:
            m += 1
        music_data = Music_Data(score=m, music_id=i, user_id=1)
        session.add(music_data)
    session.commit()
    return "finished"

@app.route('/test2', methods=['GET'])
def test2():
    music_data = session.query(Music.id, Music_Data.music_id).filter(Music.id == Music_Data.music_id).filter(Music_Data.score>=0).filter(Music.category==1)
    print(str(music_data))
    result = ""
    for item in music_data:
        result += str(item.id) + "<br>"

    return result



if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(port=5000)
