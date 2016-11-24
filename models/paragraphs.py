# coding: utf8
from database import db


class Paragraph(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    offset = db.Column(db.Integer)
    content = db.Column(db.Text)
    content_type = db.Column(db.Integer)
    chapter = db.Column(db.Integer)
    section = db.Column(db.Integer)
    subsection = db.Column(db.Integer)

    def __init__(self, book_id, offset, content, content_type, chapter, section, subsection):
        self.book_id = book_id
        self.offset = offset
        self.content = content
        self.content_type = content_type
        self.chapter = chapter
        self.section = section
        self.subsection = subsection

    def __repr__(self):
        return '<Paragraph %r>' % self.id
