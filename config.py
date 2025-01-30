import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///car_rental.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False