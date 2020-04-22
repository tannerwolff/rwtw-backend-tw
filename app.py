from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
import os
DB_URI = os.environ.get("DB_URI")
ADMIN_NAME = os.environ.get("ADMIN_NAME")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']= DB_URI

heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route('/auth', methods=['POST'])
def sign_in():
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return('LOGGED_IN')
    else:
        return("NOT_LOGGED_IN")


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key = True)
    name = ADMIN_NAME
    email = ADMIN_EMAIL
    password = ADMIN_PASSWORD


class Blog(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable=False)
    blog_status = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String, nullable=False)
    featured_image_url = db.Column(db.String, nullable=False)


    def __init__(self, title, blog_status, content, featured_image_url):
        self.title = title
        self.blog_status = blog_status
        self.content = content
        self.featured_image_url = featured_image_url

    def __repr__(self):
        return f"title {self.title}"

@app.route("/")
def home():
    return"<h1>Hi from flask </h1>"

@app.route('/blog/input', methods=["POST"])
def blogs_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        blog_status = post_data.get('blog_status')
        content = post_data.get('content')
        featured_image_url = post_data.get('featured_image_url')
        reg = Blog(title, blog_status, content, featured_image_url)
        db.session.add(reg)
        db.session.commit()
        return jsonify('Data Posted')
    return jsonify('Something went terribly wrong')
    
@app.route("/blogs", methods=['GET'])
def return_blogs():
    all_blogs = db.session.query(Blog.id, Blog.title, Blog.blog_status, Blog.content, Blog.featured_image_url).all()
    return jsonify(all_blogs)


@app.route("/blog/<id>", methods=['GET'])
def return_single_blog(id):
    one_blog = db.session.query(Blog.id, Blog.title, Blog.blog_status, Blog.content, Blog.featured_image_url).filter(Blog.id == id).first()
    return jsonify(one_blog)

@app.route("/delete/<id>", methods=['DELETE'])
def blog_delete(id):
    record = db.session.query(Blog).get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify("Deleted")

@app.route("/update_blog/<id>", methods=['PUT'])
def blog_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get('title')
        blog_status = put_data.get('blog_status')
        content = put_data.get('content')
        featured_image_url = put_data.get('featured_image_url')
        record = db.session.query(Blog).get(id)
        record.title = title
        record.blog_status = blog_status
        record.content = content
        record.featured_image_url = featured_image_url
        db.session.commit()
        return jsonify("update completed")
    return jsonify("Something went horribly wrong")


if __name__ == "__main__":
    app.debug = True
    app.run()

    