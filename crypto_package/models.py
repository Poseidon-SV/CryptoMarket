# creats data bases
# from enum import unique

# from sqlalchemy.orm import backref
from flask_login import UserMixin #useermixin f12 some impo
from crypto_package import db, login_manager
from datetime import datetime
from crypto_package import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    email = db.Column(db.String(length = 60), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 60), nullable = False)
    budget = db.Column(db.Integer(), nullable = False, default = 1000)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    currency = db.relationship('Currency', backref= 'owned_user', lazy = True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            if len(str(self.budget)) >= 8:
                f'{str(self.budget)[:-6]},{str(self.budget)[-6:-3]},{str(self.budget)[-3:]}'
            else:
                return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return self.budget

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, currency_obj):
        return self.budget >= currency_obj.price
    
    def can_sell(self, currency_obj):
        return currency_obj in self.currency
            

class Currency(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 20), nullable = False, unique = True)
    price = db.Column(db.Integer(), nullable = False)
    change = db.Column(db.Integer(), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Currnecy {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

class Market(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 20), nullable = False, unique = True)
    price = db.Column(db.Integer(), nullable = False)
    change = db.Column(db.Integer(), nullable = False)

    def __repr__(self) -> str:
        return f'Currnecy {self.name}'