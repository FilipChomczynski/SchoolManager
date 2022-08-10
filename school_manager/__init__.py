from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '2x5taA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_manager.db'
db = SQLAlchemy(app)

from school_manager import routes
from school_manager import models
from school_manager import forms
