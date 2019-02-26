from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, BIGINT, Float, Date
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
    weight = Column(Float)
    target_weight = Column(Float)
    telephone = Column(String(20))
    country = Column(String(50))
    state = Column(String(50))
    city = Column(String(50))
    session = Column(String(20))
    insert_time = Column(TIMESTAMP(True), nullable=False)


class Walk_Data(Base):
    __tablename__ = 'user_walk_data'

    id = Column(BIGINT, primary_key=True)
    walk = Column(Integer)
    date = Column(Date)

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

class Calories_Data(Base):
    __tablename__ = 'user_calorie_data'

    id = Column(BIGINT, primary_key=True)
    calorie = Column(Integer)
    date = Column(Date)

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

class Survey_Data(Base):
    __tablename__ = 'user_survey_data'

    id = Column(BIGINT, primary_key=True)
    Q1 = Column(Integer)
    Q2 = Column(Integer)
    Q3 = Column(Integer)
    Q4 = Column(Integer)
    Q5 = Column(Integer)
    Q6 = Column(Integer)
    Q7 = Column(Integer)
    Q8 = Column(Integer)
    Q9 = Column(Integer)
    Q10 = Column(Integer)
    score = Column(Integer)
    date = Column(Date)

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))






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
