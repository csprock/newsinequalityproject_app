from app import db
from datetime import datetime

class Author(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256))
    handle = db.Column(db.String(256))

    __table_args__ = (db.UniqueConstraint('firstname', 'lastname', name="u_author_firstname_lastname"),)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<Author {}_{}>".format(self.firstname, self.lastname)

    def posts(self):
        my_posts = Post.query.filter_by(author_id=self.id)
        return my_posts


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    subtitle = db.Column(db.String(256))
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def author(self):
        author = Author.query.filter_by(id=self.author_id).first()
        return author

    def __repr__(self):
        return "<Post {}>".format(self.title)
