# coding: utf8
import configparser
from flask import Flask, send_file, request, jsonify

from database import db
from models.books import Book
from models.paragraphs import Paragraph
from models.annotations import Annotation
from models.audios import Audio
from models.images import Image

app = Flask(__name__)

# load mysql config.
cf = configparser.ConfigParser()
cf.read('configs/dev.ini')
app.config['SQLALCHEMY_DATABASE_URI'] = cf.get('mysql', 'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cf.getboolean('mysql', 'SQLALCHEMY_TRACK_MODIFICATIONS')

app.app_context().push()

db.init_app(app)
db.create_all()


@app.route('/media/<md5>')
def get_image(md5):
    return jsonify()


@app.route('/audio/<md5>')
def get_audio(md5):
    return jsonify()


@app.route('/book')
def get_book_list():
    lang = request.args.get('lang', 'all')

    query = Book.query
    if lang != 'all':
        query = query.filter(Book.lang == lang)
    books = query.all()

    rt = []
    for book in books:
        rt.append(book.to_dict())

    return pack({"list": rt})


@app.route('/book/<book_id>')
def get_book(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    if book is None:
        return pack({}, False, 1)

    contents = Paragraph.query.filter(Paragraph.book_id == book.id).all()
    content_list = []
    for content in contents:
        content_info = content.to_dict()
        content_info["audioUrl"] = Audio.get_audio_filename(book.id, content.chapter)
        content_info["imageUrl"] = Image.get_image_filename(content.id)
        content_info["annotation"] = Annotation.get_annotations(content.id)
        content_list.append(content_info)

    return pack({
        "book": book.to_dict(),
        "content": content_list
    })


def pack(rt, result=True, error=0):
    if result:
        rt["result"] = "success"
    else:
        rt["result"] = "failed"
    rt["errCode"] = error
    return jsonify(rt)

if __name__ == '__main__':
    app.run(debug=True, port=8000)




