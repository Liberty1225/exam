from app import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users_employee'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.username

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    short_info = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    preferred_position = db.Column(db.String, nullable=False)
    user = db.relationship(User, backref=db.backref('users', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('users_employee.id'))

    def __repr__(self):
        return self.fullname
