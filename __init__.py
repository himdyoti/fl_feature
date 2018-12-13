from flask import  Flask,render_template
import sqlalchemy as schemy
from flask_login import LoginManager
from flask.json import JSONEncoder
from datetime import datetime
import calendar

feature_status = [
    {'name':'open', 'sid':1},
    {'name':'close', 'sid':2},
    {'name':'ready', 'sid':3},
    {'name':'cancelled', 'sid':4},
    {'name':'postponed', 'sid':5}
]

class CustomJSONEncoder(JSONEncoder):
    #http://flask.pocoo.org/snippets/119/
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass

        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config.from_pyfile('config.cfg')
from . import views
from .db import DB
__all__=['app','DB','feature_status']

if __name__=="__main__":
    app.run(host='0.0.0.0')

