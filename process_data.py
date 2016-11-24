# coding: utf8
from openpyxl import load_workbook
import pandas as pd
import re

from app import app
from database import db
from models.books import Book
from models.paragraphs import Paragraph
from models.images import Image
from models.annotations import Annotation

BOOK_ID = 1
TEXT_TYPE_MAP = {
    u"标题":0,
    u"序言":1,
    u"正文":2
}

db.init_app(app)
db.create_all()

# load sheets.
# TODO： 增加一个音频对应的sheet，不过这个工作量不大
wb = load_workbook('doc.xlsx')
for data in wb.get_sheet_names():
    print data

df = pd.DataFrame(wb.worksheets[0].values)
df.columns = df.iloc[0]
df = df.reindex(df.index.drop(0))

image_df = pd.DataFrame(wb.worksheets[1].values)
image_df.columns = image_df.iloc[0]
image_df = image_df.reindex(image_df.index.drop(0))


# 添加书籍记录
def add_book():
    book = Book(u"侧记", "zh-CN", 1.12, 0, "学诚大和尚的生平事迹")
    db.session.add(book)
    db.session.commit()


# 添加段落信息
def add_paragraphs():
    df.dropna(axis=1, how='all').apply(parse_paragraph, axis=1)
    db.session.commit()


# 添加图片信息
def add_images():
    image_df.dropna(axis=1, how='all').apply(parse_image, axis=1)
    db.session.commit()


# 添加注释信息
def add_annotations():
    df.dropna(axis=1, how='all').apply(parse_annotation, axis=1)
    db.session.commit()


# 解析章节信息
# 3-1-1 return [3, 1, 1]
# 3-1   return [3, 1]
def parse_section(section):
    return section.split("-")[:2] + ["-".join(section.split("-")[2:])]


# 解析段落信息
def parse_paragraph(x):
    offset = x.get(u"时间", 0)
    content = x.get(u"文本内容")
    ctype = TEXT_TYPE_MAP.get(x.get(u"文本类型"))
    position = x.get(u"段落")
    chapter, section, subsection = parse_section(x.get(u"章节"))
    paragraph = Paragraph(BOOK_ID, offset, content, ctype, chapter, section, subsection, position)
    db.session.add(paragraph)


# 解析图片信息
def parse_image(x):
    md5 = x.get(u"图片文件名")
    chapter, section, subsection = parse_section(x.get(u"章节"))
    p_id = x.get(u"段落") or 0
    paragraph = Paragraph.query.filter(Paragraph.chapter == chapter,
                                       Paragraph.section == section,
                                       Paragraph.subsection == subsection).all()[p_id]
    paragraph_id = paragraph.id
    desc = x.get(u"图片说明")
    image = Image(paragraph_id, md5, desc)
    db.session.add(image)


# 解析注释，返回list，每个元素是一个(关键字, 解释)
def parse_keyword(content):
    annotations = []
    pattern = r"\[\d+\].+?:{1}.+?\.{1}\s*?"
    keyword_pattern = "\[\d+\](.+?):(.+?)\."
    rst = re.compile(pattern, re.M).findall(content)
    for idx, annotation in enumerate(rst):
        rt = re.compile(keyword_pattern, re.M).search(annotation)
        annotations.append((idx + 1, rt.group(1).strip(), rt.group(2).strip()))
    return annotations


# 解析注释
def parse_annotation(x):
    content = x.get(u"注释")
    if content is None:
        return
    chapter, section, subsection = parse_section(x.get(u"章节"))
    p_id = x.get(u"段落") or 0  # 0 for title
    paragraph = Paragraph.query.filter(Paragraph.chapter == chapter,
                                       Paragraph.section == section,
                                       Paragraph.subsection == subsection).all()[p_id]
    paragraph_id = paragraph.id
    for annotation in parse_keyword(content):
        idx, keyword, desc = annotation
        anno = Annotation(paragraph_id, keyword, desc, idx)
        db.session.add(anno)

add_book()
add_paragraphs()
add_annotations()
add_images()
