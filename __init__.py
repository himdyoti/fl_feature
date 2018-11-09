from flask import  Flask,render_template
import sqlalchemy as schemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
import fl_britecore.views
from .db import DB
__all__=['app','DB']

