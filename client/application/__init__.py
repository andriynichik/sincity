from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="d4MQDYRuUw",
    WTF_CSRF_SECRET_KEY="h3PxyC5QSO"
))

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

import application.france
import application.index