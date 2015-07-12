# project/models.py


import datetime

from project import db, bcrypt

'''
User Roles:
    Anonymous:  User who is not logged in. Cannot see artists
    User:       Allowed to view artists and make purchases
    Artist:     Allowed to view artists/make purchases/create products
    Admin:      Full access.

    The following are per the Flask Web Development book, page 112
'''
class Permission:
    BUY = 0x01
    SELL = 0x02
    ADMINISTER = 0x03


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
            roles = {
                'User': (Permission.BUY, True),
                'Artist': (Permission.BUY | Permission.SELL, True),
                'Admin': (0xff, False)
            }
            for r in roles:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    about_me = db.Column(db.Text())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    products = db.relationships('Product', backref='artist', lazy=dynamic)

    def __init__(self, email, password, confirmed,
                 admin=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)

