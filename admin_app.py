from datetime import date
from flask import Flask, render_template, request, redirect, url_for, Response, session, flash
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
# import _imaging
# import Image
#from PIL.Image import core as image
# from PIL.Image import core as _imaging
# # from PIL import Image, ImageDraw
from wtforms import StringField, PasswordField
from wtforms import form
from wtforms.fields import DateField
from wtforms.fields.core import RadioField
import cv2
import json
import requests
import pymongo
from wtforms.form import Form
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

import random

app = Flask(__name__, template_folder='.')
mail = Mail(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'project',
    'host': 'mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority',
    'port': 27017
}
# mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dragonsairam.sai@gmail.com'
app.config['MAIL_PASSWORD'] = '896209Sa!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SECRET_KEY'] = "HELLO_WORLD"
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField()
    password = db.StringField()
    name = db.StringField()
    rollno = db.StringField()
    cate = db.StringField()


class facial(UserMixin, db.Document):
    meta = {'collection': 'rec1'}
    rollno = db.StringField()
    face_pixels = db.ListField()

