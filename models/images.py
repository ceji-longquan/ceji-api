# coding: utf8
from database import db


class Image(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    paragraph_id = db.Column(db.Integer)
    md5 = db.Column(db.String(40), unique=True)
    desc = db.Column(db.String(40))

    def __init__(self, paragraph_id, md5, desc):
        self.paragraph_id = paragraph_id
        self.md5 = md5
        self.desc = desc

    def __repr__(self):
        return '<Image %r>' % self.id

    @staticmethod
    def get_image_filename(paragraph_id):
        images = Image.query.filter(Image.paragraph_id == paragraph_id).all()
        image_list = []
        for image in images:
            image_list.append("/image/%s" % image.md5)
        return image_list
