from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    rental_cost = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('offices.id'))

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone_no = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image = db.Column(db.String(200))  
