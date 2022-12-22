from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

tags = db.Table('post_tags',
    db.Column('post_id',db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref = 'users',
        lazy = 'dynamic'
    )

    def __init__(self, username) -> None:
        self.username = username

    def __repr__(self) -> str:
        return "<User '{}'>".format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    comments  = db.relationship(
        'Comment',
        backref = 'post',
        lazy = 'dynamic'
    )
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    tags = db.relationship(
        'Tag',
        secondary = tags,
        backref = db.backref('posts', lazy = 'dynamic')
    )

    def __init__(self, title) -> None:
        self.title = title

    def __repr__(self) -> str:
        return "<Post '{}'>".format(self.title)
        
class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self) -> str:
        return "<Comment '{}'>".format(self.text[:15])

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))

    def __init__(self, title) -> None:
        self.title = title

    def __repr__(self) -> str:
        return "<Tag '{}'>".format(self.title)

@app.route('/')
def home():
    return '<h1> Hello Word ! </h1>'

if __name__ == '__main__':
    app.run()