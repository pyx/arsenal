"""arsenal.models - models of arsenal"""

from datetime import datetime

from bleach import linkify
from flask import url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from markdown import markdown
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class CreatedOnMixin(object):
    created_on = db.Column(db.DateTime, default=datetime.utcnow)


class UpdatedOnMixin(object):
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Post(CreatedOnMixin, UpdatedOnMixin, db.Model):
    """Post"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)

    author_id = db.Column(db.ForeignKey('user.id'), index=True)
    topic_id = db.Column(db.ForeignKey('topic.id'), index=True)

    def update_html(self):
        self.updated_on = datetime.utcnow()
        exts = [
            'markdown.extensions.extra',
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            'markdown.extensions.toc',
            'markdown.extensions.wikilinks',
        ]
        self.content_html = linkify(markdown(self.content, extensions=exts))


class Topic(CreatedOnMixin, UpdatedOnMixin, db.Model):
    """Topic thread"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    is_sticky = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.ForeignKey('user.id'), index=True)
    posts = db.relationship(
        'Post', backref='topic',
        lazy='dynamic', cascade='all,delete', order_by='Post.id')

    @property
    def last_post(self):
        return self.posts[-1]

    @property
    def post_count(self):
        return self.posts.count()

    @property
    def url(self):
        return url_for('forum.topic', id=self.id)


class User(UserMixin, CreatedOnMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)

    topics = db.relationship(
        'Topic', backref='author', lazy='dynamic', order_by='Topic.id')
    posts = db.relationship(
        'Post', backref='author', lazy='dynamic', order_by='Post.id')

    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def url(self):
        return url_for('user.profile', id=self.id)


def init_app(app):
    db.init_app(app)
