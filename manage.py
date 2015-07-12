# manage.py
import os
import unittest
import coverage
import datetime
import stripe

import flask_admin as admin
from flask_admin.contrib import sqla 
from flask_sqlalchemy import SQLAlchemy

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


COV = coverage.coverage(
        branch=True,
        include='project/*',
        omit=['*/__init__.py', '*/config/*']
    )
COV.start()

from project import app, db
from project.models import User, Role

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(os.environ['APP_SETTINGS'])


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    COV.erase()


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        email="ad@min.com",
        password="admin",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now())
    )
    db.session.commit()

'''
Flask Admin Instantiation

def create_app():
    app = Flask('flask_app')

    admin = Admin()

    admin.add_view(sqla.ModelView(models.User, db.session))    
    admin.init_app(app)

    return app
'''

if __name__ == '__main__':
    manager.run()


