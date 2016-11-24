# coding: utf8
from database import db


class Audio(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer)
    md5 = db.Column(db.String(40), unique=True)

    def __init__(self, chapter_id, md5):
        self.chapter_id = chapter_id
        self.md5 = md5

    def __repr__(self):
        return '<Audio %r>' % self.id