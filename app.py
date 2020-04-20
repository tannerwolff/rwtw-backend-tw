from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']=''

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


if __name__ == "__main__":
    app.debug = True
    app.run()

    