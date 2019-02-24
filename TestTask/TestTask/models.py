from datetime import datetime
from flask_login import UserMixin
from TestTask import db, login
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Integer, index=True, default=10000)
    bought_commodities = db.relationship('BoughtCommodity', backref='buyer', lazy='dynamic')

    def __repr__(self):
        return 'User {0} (id: {1})'.format(self.email, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    commodities = db.relationship('Commodity', backref='catry', lazy='dynamic')

    def __repr__(self):
        return 'Category {0} (id: {1})'.format(self.name, self.id)

class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    price = db.Column(db.Integer, index=True)
    rest = db.Column(db.Integer, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    bought_commodities = db.relationship('BoughtCommodity', backref='comty', lazy='dynamic')

    def __repr__(self):
        return 'Commodity {0} (category: {1}, price: {2}, rest: {3})'.format(self.name, self.catry.name, self.price, self.rest)

class BoughtCommodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    count = db.Column(db.Integer, index=True)

    def __repr__(self):
        return 'BoughtCommodity {0} (buyer: {1}, commodity: {2}, {3}*{4}={5})'.format(self.id, self.buyer.email, self.comty.name, self.comty.price, self.count, self.comty.price*self.count)