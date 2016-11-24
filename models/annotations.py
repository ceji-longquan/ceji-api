# coding: utf8
from database import db


class Annotation(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer)
    keyword = db.Column(db.String(200))
    desc = db.Column(db.Text)
    index = db.Column(db.Integer)

    def __init__(self, paragraph_id, keyword, desc, index):
        self.paragraph_id = paragraph_id
        self.keyword = keyword
        self.desc = desc
        self.index = index

    def __repr__(self):
        return '<Annotation %r>' % self.id

    @staticmethod
    def get_annotations(paragraph_id):
        annotations = Annotation.query.filter(Annotation.paragraph_id == paragraph_id).all()
        annotation_list = []
        for annotation in annotations:
            annotation_list.append(annotation.to_dict())
        return annotation_list

    def to_dict(self):
        return {
            "code": self.index,
            "target": self.keyword,
            "explain": self.desc
        }
