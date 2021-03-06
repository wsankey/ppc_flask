# project/__init__.py


#################
#### imports ####
#################

import os
import psycopg2
import urlparse
import stripe

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension

from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
################
#### config ####
################

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'memcached'

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config.from_object(os.environ['APP_SETTINGS'])


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
from project.user.views import profile_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(profile_blueprint)


####################
#### flask-login ####
####################

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"

from project.models import User
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



admin = Admin(app, name='Pet Portrait Club', template_mode='bootstrap3')
admin.add_view(ModelView(models.User, db.session))