from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# Контактная книга
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Person(name='{self.name}', birthday='{self.birthday}', details='{self.details}', phone='{self.phone}', address='{self.address}')"


# Заметки
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    notes = db.relationship('Note', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'


# Ежедневник
class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', backref='rank', lazy=True)

    def __repr__(self):
        return f'<Rank {self.name}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_tag', backref='tags', lazy=True)

    def __repr__(self):
        return f'<Tag {self.name}>'


post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'), nullable=False)

    def repr(self):
        return f'<Post {self.title}>'

    @classmethod
    def newest_first(cls):
        return cls.query.order_by(cls.date.desc())
