from flask import Flask, request, make_response
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Walk_Data, Calories_Data, Survey_Data, Music_Data, Video_Data, Music, Video

import json
import hashlib
import time, random

import recommendation

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
        if user is None or hash.hexdigest() != user.password:
            response['msg'] = "Wrong username or password"
            response['code'] = "200"
            return make_response(json.dumps(response), 200)
        elif hash.hexdigest() == user.password:
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
            response['msg'] = "Unknown Error"
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
                        response['msg'] = "No Data on such Types"
                        response['data'] = data
                        response['code'] = "200"
                        return make_response(json.dumps(response), 200)
                    response['msg'] = "User Information " + str(request.form['data_type']).capitalize() \
                                      +" Data Get Successful"
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
                    data = {}
                    response['msg'] = "No Data on such Types"
                    response['data'] = data
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


@app.route('/user/<int:user_id>/recomendation', methods=['GET'])
def recomendation(user_id):
    response = {}
    # survey_data = session.query(func.avg(Survey_Data.score).label('average')).filter(Survey_Data.user_id==user_id).filter(Survey_Data.date>"2019-1-1").filter(Survey_Data.date<"2019-12-31").scalar()
    survey_data = session.query(func.avg(Survey_Data.score).label('average')).filter(Survey_Data.user_id==user_id).scalar()
    today_survey_data = session.query(Survey_Data.score).filter(Survey_Data.user_id==user_id).filter(Survey_Data.date==time.strftime('%Y-%m-%d')).scalar()
    user_data = session.query(User.prefer).filter(User.id==user_id).first()

    if user_data is not None:
        prefer = user_data[0]
    else:
        prefer = ""
    if survey_data is None or today_survey_data is None:
        response['msg'] = "User has No Survey Data"
        response['code'] = "200"
        return make_response(json.dumps(response), 200)
    average_score = float(survey_data)
    score = float(today_survey_data)

    user_dict = {}
    user_dict['prefer'] = prefer
    user_dict['average_score'] = average_score
    user_dict['score'] = score

    recom = recommendation.recommendation(user_id, user_dict)
    category = recom.estimate()

    item_dict = {"music":{}, "video":{}}
    music_data = session.query(Music.id, Music_Data.music_id, Music_Data.user_id, Music_Data.score).filter(Music.id == Music_Data.music_id).filter(Music.category==category)
    video_data = session.query(Video.id, Music_Data.music_id, Video_Data.user_id, Video_Data.score).filter(Video.id == Video_Data.video_id).filter(Video.category==category)

    for md in music_data:
        if md.id not in item_dict['music']:
            item_dict['music'][md.id] = {md.user_id: md.score}
        else:
            item_dict['music'][md.id][md.user_id] = md.score

    for vd in video_data:
        if vd.id not in item_dict['video']:
            item_dict['video'][vd.id] = {vd.user_id: vd.score}
        else:
            item_dict['video'][vd.id][vd.user_id] = vd.score

    result = recom.recommend(item_dict)

    if result[0] == 'music':
        recomend_data = session.query(Music).filter_by(id=result[1]).first()
    elif result[0] == 'video':
        recomend_data = session.query(Video).filter_by(id=result[1]).first()
    else:
        response['msg'] = "No Recomendation Type"
        response['code'] = "200"
        return make_response(json.dumps(response), 200)

    data = {}
    data['title'] = recomend_data.title
    data['link'] = recomend_data.link

    response['msg'] = "Recomendation Successful"
    response['data'] = data
    response['code'] = "200"
    return make_response(json.dumps(response), 200)


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

@app.route('/generate_fake_survey_data', methods=['GET'])
def generate_fake_survey_data():
    for u in range(1,100+1):
        for i in range(1, 12+1):
            for j in range(1, 30+1):
                survey_data = Survey_Data(score=random.randint(1,4),date="2019-" + str(i) + "-" + str(j), user_id=u)
                session.add(survey_data)
    session.commit()
    return make_response("OK!", 200)

@app.route('/generate_fake_music_data', methods=['GET'])
def generate_fake_music_data():
    for i in range(1, 10+1):
        for j in range(4, 100+1):
            music_data = Music_Data(score=random.randint(1,4),date=time.strftime('%Y-%m-%d'), user_id=j, music_id=i)
            session.add(music_data)
    session.commit()
    return make_response("OK!", 200)

@app.route('/generate_fake_video_data', methods=['GET'])
def generate_fake_video_data():
    for i in range(1, 10+1):
        for j in range(4, 100+1):
            video_data = Video_Data(score=random.randint(1,4),date=time.strftime('%Y-%m-%d'), user_id=j, video_id=i)
            session.add(video_data)
    session.commit()
    return make_response("OK!", 200)

@app.route('/generate_fake_user', methods=['GET'])
def generate_fake_user():
    for j in range(1, 10000+1):
        user = User(username=str(random.randint(100000,999999)), password=str(random.randint(100000,999999)))
        session.add(user)
    session.commit()
    return make_response("OK!", 200)

if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(port=5000)
