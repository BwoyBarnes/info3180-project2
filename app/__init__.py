from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "3184cf50b884fd2828b2a084ac04d518f7c4f4e8f22f416a"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://info3180:password@localhost/project-2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
UPLOAD_FOLDER = './app/static/uploads'
DEFAULT_BIO = 'This person has not entered a bio.'


db = SQLAlchemy(app)
bcryptHash = Bcrypt(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
