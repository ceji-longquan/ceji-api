# coding: utf8
import configparser
from flask import Flask, send_file

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
    pass


@app.route('/book')
def get_book_list():
    pass


@app.route('/book/<id>')
def get_book(id):
    pass


if __name__ == '__main__':
    app.run(debug=True, port=8000)




