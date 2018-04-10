# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from convert import Convert

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:gwf1997@localhost:3306/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
db = SQLAlchemy(app)
api = Api(app)

from datetime import datetime

class News(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(100))
    image = db.Column(db.String(100))
    theme_id = db.Column(db.Integer)

    def to_json(self):
        return {
            'id': self.id,
            'created': self.created.strftime("%Y-%m-%d %H:%M:%S"),
            'title': self.title,
            'image': self.image,
            'theme_id': self.theme_id
        }


class NewsDetail(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    created = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.String(1000))
    image = db.Column(db.String(100))

    def to_json(self):
        return {
            'id': self.id,
            'news_id': self.news_id,
            'created': self.created.strftime("%Y-%m-%d %H:%M:%S"),
            'content': self.content,
            'image': self.image
        }

class NewsList(Resource):
    def get(self):
        news_list = []
        news = News.query.limit(10).all()
        for n in news:
            news_list.append(n.to_json())
        return {
            'stories': news_list
        }

class NewsDetailContent(Resource):
    def get(self, news_id):
        news_detail = NewsDetail.query.filter_by(news_id=news_id).first()
        return news_detail.to_json()

class ThemeNewsList(Resource):
    def get(self, theme_id):
        news=NewsDetail.query.filter_by(theme_id=theme_id).all()
        news_list=[]
        for n in news:
            news_list.append(n.to_json)
        return {
            'stories': news_list
        }

api.add_resource(NewsList, '/api/news/latest')
api.add_resource(NewsDetailContent, '/api/news/<news_id>')
api.add_resource(ThemeNewsList, '/api/news/theme/<theme_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)