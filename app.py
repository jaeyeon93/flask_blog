# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for, request, session
from models.user import User
from common.database import Database

app = Flask(__name__)
app.secret_key = "jaeyeon"
# __name__ 빌트인변수? '__main__'을 포함한다.


@app.route('/') #www.mysite.com/api/
def hello_method():
    return render_template('login.html')

@app.before_first_request
# login을 하기전에 이것을 먼저 실행한다
def initialize_database():
    Database.initialize()


@app.route('/login', methods=['GET','POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    # request.from['name']을 통해 값을 받아온다 html, input태그에서 id가 아닌, name값을 넣어야한다
    if User.login_valid(email,password):
        User.login(email)
    return render_template('profile.html', email=session['email'])
    # profile.html파일이 session['email']을 엑세스할 수 있게한다


if __name__ == '__main__':
    app.run(debug=True,port=4995)
