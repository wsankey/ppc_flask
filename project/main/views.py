# project/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint
from flask.ext.login import login_required
import stripe
import os
stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
def home():
    return render_template('main/index.html')

@main_blueprint.route('/artists')
#@login_required
def artists():
	return render_template('main/artists.html', key=stripe_keys['publishable_key'])
