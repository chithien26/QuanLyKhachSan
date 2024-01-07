from flask import Flask
from urllib.parse import quote

app = Flask(__name__)
# app.secret_key = "BG\xeb\xdd\t\xf1\x93\xbeWp\xbb\xffla V"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4' % quote ('chithien26@')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app=app)
# login = LoginManager(app=app)
# admin = Admin(app=app, name='QUẢN LÝ KHÁCH SẠN', template_mode='bootstrap5')