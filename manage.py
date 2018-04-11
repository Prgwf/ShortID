# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, session, flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
import re
from convert import Convert

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:token@localhost:3306/shortid_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
app.config['SECRET_KEY'] = 'dont do badthings to me please'
db = SQLAlchemy(app)
api = Api(app)
bootstrap = Bootstrap(app)

radix_transfer = Convert()

class RawURL(db.Model):
    __tablename__ = 'urls'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(4096))

    def to_json(self):
        return {
            'url': self.url,
            's_url' : radix_transfer.toStr(self.uid)
        }


class URLForm(FlaskForm):
    # validators.URL() shit...
    url = StringField('URL', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')
    output = StringField()

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if request.method == 'GET':
        return render_template('index.html', form=form)

    # todo 'front end|architecture|RESTful'
    if request.method == 'POST':
        if form.validate_on_submit():
            raw_url = form.url.data
            pattern = re.compile(r'://')
            t = pattern.split(raw_url)
            processed_url = t[1] if (len(t) > 1) else t[0]

            print(processed_url)

            info = RawURL.query.filter_by(url=form.url.data).first()
            # graceful byebye~
            if info is None:
                info = RawURL(url=processed_url)
                db.session.add(info)
                db.session.commit()
            ret_url = url_for('index', _external=True) + radix_transfer.toStr(info.uid)
            form.url.data = raw_url
            form.output.data = ret_url
        return render_template('index.html', form=form)


@app.route('/<string:str>')
def let_s_jump(str):
    r = url_for('let_s_jump', _external=True, str=str)
    print(r)
    uid = radix_transfer.toNum(str)
    line = RawURL.query.filter_by(uid=uid).first()
    if line is None:
        page_not_found()
    else :
        # todo redirect urls like baidu.com
        return redirect('https://'+line.url)

# todo direct jump from url...
@app.route('/api/<path:url>')
def direct_jump(url):
    pass

if __name__ == '__main__':
    db.create_all()
    app.run()