from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)

class Hospital(db.Model):
    pno = db.Column(db.Integer(), primary_key=True)
    pname = db.Column(db.String(20), unique=False, nullable=False)
    pgender = db.Column(db.String(5), unique=False, nullable=False)
    page = db.Column(db.Integer(),unique=False, nullable=False)
    pward = db.Column(db.String(20),unique=False, nullable=False)
    pstatus =db.Column(db.String(20))
