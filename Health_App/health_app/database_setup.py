from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, BIGINT, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(32), nullable=False)
    gender = Column(Integer, nullable=True)
    age = Column(Integer)
    major = Column(String(50))
    prefer = Column(String(50))
    weight = Column(Float)
    target_weight = Column(Float)
    telephone = Column(String(20))
    country = Column(String(50))
    state = Column(String(50))
    city = Column(String(50))
    session = Column(String(20))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'age': self.age,
            'major': self.major,
            'prefer': self.prefer,
            'weight': self.weight,
            'target_weight': self.target_weight,
            'telephone': self.telephone,
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'session': self.session
        }


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    link = Column(Text)
    category = Column(Integer)
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'category': self.category
        }


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    link = Column(Text)
    category = Column(Integer)
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'category': self.category
        }

class Walk_Data(Base):
    __tablename__ = 'user_walk_data'

    id = Column(BIGINT, primary_key=True)
    walk = Column(Integer)
    date = Column(Date)

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'walk': self.walk,
            'date': str(self.date),
            'user_id': self.user_id
        }

class Calories_Data(Base):
    __tablename__ = 'user_calorie_data'

    id = Column(BIGINT, primary_key=True)
    calorie = Column(Integer)
    date = Column(Date)

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'calorie': self.calorie,
            'date': str(self.date),
            'user_id': self.user_id
        }


class Survey_Data(Base):
    __tablename__ = 'user_survey_data'

    id = Column(BIGINT, primary_key=True)
    score = Column(Integer)
    date = Column(Date)

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'date': str(self.date),
            'user_id': self.user_id
        }


class Music_Data(Base):
    __tablename__ = 'user_music_data'

    id = Column(BIGINT, primary_key=True)
    score = Column(Integer)
    date = Column(Date)

    music = relationship(Music)
    music_id = Column(Integer, ForeignKey('music.id'))
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'date': str(self.date),
            'music_id': self.music_id,
            'user_id': self.user_id
        }

class Video_Data(Base):
    __tablename__ = 'user_video_data'

    id = Column(BIGINT, primary_key=True)
    score = Column(Integer)
    date = Column(Date)

    video = relationship(Video)
    video_id = Column(Integer, ForeignKey('video.id'))
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))
    insert_time = Column(TIMESTAMP(True), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'score': self.score,
            'date': self.date,
            'video_id': self.video_id,
            'user_id': self.user_id
        }


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

Base.metadata.create_all(engine)
