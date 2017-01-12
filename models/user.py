# -*- coding:utf-8 -*-
from models.blog import Blog
from flask import session

__author__='jaeyeon'
from common.database import Database
import uuid, datetime

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id= uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls,email):
        data = Database.find_one("users",{"email": email})
        if data is not None:
            return cls(**data)

        return None

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users",{"_id": _id})

    @staticmethod
    def login_valid(email, password):
        # User.Login_valid("jaeyeon@naver.com","1234")
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password

    @classmethod
    # 만약에 user클래스 이름을 바꾸면 클래스이름을 바꿀 필요가 없기때문에 cls를 사용한다
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User does not exist, so we can create it
            new_user = User(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists
            return False
    @staticmethod
    def login(user_email):
        # Login_valid has already been called.
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)
    # find_by_author_id return list of blog object.

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()
    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            'email': self.email,
            '_id': self._id,
            'password':self.password
        }

    def save_to_mongo(self):
        Database.insert("users",self.json())




