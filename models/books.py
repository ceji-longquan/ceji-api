# coding: utf8
from database import db


class Book(db.Model):
    __table_args__ = ( db.UniqueConstraint('name', 'lang', 'version'), {"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lang = db.Column(db.String(20))
    version = db.Column(db.Integer)
    cover = db.Column(db.Integer)
    desc = db.Column(db.Text)

    def __init__(self, name, lang, version, cover, desc):
        self.name = name
        self.lang = lang
        self.version = version
        self.cover = cover
        self.desc = desc

    def __repr__(self):
        return '<Book %r>' % self.id
