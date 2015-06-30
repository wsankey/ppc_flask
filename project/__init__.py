# project/__init__.py


#################
#### imports ####
#################

import os
import psycopg2
import urlparse

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy


################
#### config ####
################

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.wsankey,
    password=url.Julia1020,
    host=url.hostname,
    port=url.port
)
#app.config.from_object(os.environ['APP_SETTINGS'])
#print os.environ['APP_SETTINGS']

####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)


####################
#### blueprints ####
####################

from project.main.views import main_blueprint
from project.user.views import user_blueprint
from project.artist.views import artist_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(artist_blueprint)

####################
#### flask-login ####
####################

from project.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


########################
#### error handlers ####
########################

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
