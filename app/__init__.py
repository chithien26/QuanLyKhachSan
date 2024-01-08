from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.secret_key = "BG\xeb\xdd\t\xf1\x93\xbeWp\xbb\xffla V"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/quanlykhachsan?charset=utf8mb4' % quote ('chithien26@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name='QUẢN LÝ KHÁCH SẠN', template_mode='bootstrap4')
# login = LoginManager(app=app)
