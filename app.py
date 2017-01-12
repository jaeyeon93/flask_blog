# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for, request, session, make_response
from models.user import User
from common.database import Database
from models.blog import Blog
from models.post import Post

app = Flask(__name__)
app.secret_key = "jaeyeon"
# __name__ 빌트인변수? '__main__'을 포함한다.

@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login') #www.mysite.com/api/login
def login_template():
    return render_template('login.html')

@app.route('/register') # www.mysite.com/api/register
def register_template():
    return render_template('register.html')

@app.before_first_request
# login을 하기전에 이것을 먼저 실행한다
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['GET','POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    # request.from['name']을 통해 값을 받아온다 html, input태그에서 id가 아닌, name값을 넣어야한다
    if User.login_valid(email,password):
        User.login(email)
    else:
        session['email'] = None
    return render_template('profile.html', email=session['email'])
    # profile.html파일이 session['email']을 엑세스할 수 있게한다

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route(('/blogs'))
def user_blogs(user_id=None):
    # /blogs는 id값이 none일때, 위에루트는 아이디값이 있을때 사용
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html')
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))


if __name__ == '__main__':
    app.run(debug=True,port=4995)
