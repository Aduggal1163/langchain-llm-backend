from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True) #index means it will increase performance a lil bit whenever we search using id
    username = Column(String(50), unique=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)