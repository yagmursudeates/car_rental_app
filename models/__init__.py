from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "car_rental.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    from .models import home, login, office_info, search_results, car_detail, show_office_cars
    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(office_info)
    app.register_blueprint(search_results)
    app.register_blueprint(car_detail)
    app.register_blueprint(show_office_cars)

    # Veritabanı tablolarını oluştur
    with app.app_context():
        db.create_all()


    return app
