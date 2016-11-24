# coding: utf8
from database import db


class Annotation(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer)
    keyword = db.Column(db.String(200))
    desc = db.Column(db.Text)

    def __init__(self, paragraph_id, keyword, desc):
        self.paragraph_id = paragraph_id
        self.keyword = keyword
        self.desc = desc

    def __repr__(self):
        return '<Annotation %r>' % self.id