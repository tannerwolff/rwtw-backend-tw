from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://lxqdmdrbsnxzrh:7a103b10854944a597e55d2bbe9e639869dd38f47f4bfcc9f530d6d2b6dd44dd@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d7u3fc26h5icob'

heroku = Heroku(app)
db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    blog_status = db.Column(db.String(10))
    content = db.Column(db.String)
    featured_image_url = db.Column(db.String)

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

    