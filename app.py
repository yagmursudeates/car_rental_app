from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.models import db, User, Car, Office
from helpers.auth_handler import hash_password, check_password, is_authenticated, get_current_user
from helpers.validators import validate_user_registration
from helpers.google_maps import get_office_locations
from config import Config
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, jsonify
from models.models import db, Office

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

LANGUAGES = {
    "en": {
        "welcome": "Welcome to Car Rental",
        "pickup_office": "Pickup Office",
        "pickup_date": "Pickup Date",
        "pickup_time": "Pickup Time",
        "return_office": "Return Office",
        "return_date": "Return Date",
        "return_time": "Return Time",
        "rent_for_days": "Rent",
        "logout": "Logout",
        "login": "Login",
        "register": "Register",
        "office_map": "Office Map",
        "no_cars_found": "No cars found matching your criteria.",
        "results": "Results",
        "show_cars": "Show Cars",
        "back_to_home": "Back to Home",
        "sort_by": "Sort By",
"transmission": "Transmission",
"cost": "Cost",
"mileage": "Mileage",
"age": "Age",
"rental_cost": "Rental Cost",
"filter_transmission": "Filter by Transmission",
"all": "All",
"automatic": "Automatic",
"manual": "Manual",
"sort_order": "Sort Order",  
"ascending": "Ascending",   
"descending": "Descending",

    },
    "tr": {
        "welcome": "Araba Kiralama'ya Hoşgeldiniz",
        "pickup_office": "Teslim Alma Ofisi",
        "pickup_date": "Teslim Alma Tarihi",
        "pickup_time": "Teslim Alma Saati",
        "return_office": "İade Ofisi",
        "return_date": "İade Tarihi",
        "return_time": "İade Saati",
        "rent_for_days": "X Günlük Kirala",
        "logout": "Çıkış Yap",
        "login": "Giriş Yap",
        "register": "Kayıt Ol",
        "office_map": "Ofis Haritası",
        "no_cars_found": "Aradığınız kriterlere uygun araba bulunamadı.",
        "results": "Sonuçlar",
        "show_cars": "Arabaları Göster",
        "back_to_home": "Ana Sayfaya Dön",
        "sort_order": "Sıralama Düzeni",  
"ascending": "Artan",             
"descending": "Azalan",          
        
    },
}

@app.context_processor
def inject_is_authenticated():
    return dict(is_authenticated=is_authenticated)

def create_sample_data():
    if not Office.query.first():
        offices_data = [
            {"name": "Izmir Bornova Office", "location": "Izmir", "address": "123 Izmir St.", "phone_no": "05362487550", "latitude": 38.4664, "longitude": 27.2192, "image": "images/office1.jpeg"},
            {"name": "Istanbul Kadıköy Office", "location": "Istanbul", "address": "456 Istanbul St.", "phone_no": "05211346578", "latitude": 40.9886, "longitude": 29.0270, "image": "images/office2.jpeg"},
            {"name": "Ankara Kızılay Office", "location": "Ankara", "address": "611 Ankara St.", "phone_no": "05918347657", "latitude": 39.9334, "longitude": 32.8597, "image": "images/office3.jpeg"},
            {"name": "Izmır Buca Office", "location": "Izmır", "address": "578 Izmır St.", "phone_no": "05347812130", "latitude": 38.4192, "longitude": 27.1741, "image": "images/office4.jpeg"},
            {"name": "Istanbul Tuzla Office", "location": "Istanbul", "address": "900 Istanbul St.", "phone_no": "05623145682", "latitude": 40.8700, "longitude": 29.3075, "image": "images/office5.jpeg"},
        ]

        for office_data in offices_data:
            office = Office(**office_data)
            db.session.add(office)
            db.session.commit()

        offices = Office.query.all()
        car_data = [
            {"name": "Audi A1", "transmission": "Automatic", "cost": 30000, "deposit": 5000, "mileage": 15000, "age": 3, "rental_cost": 100, "image": "images/car1.jpeg"},
            {"name": "Mercedes Benz E", "transmission": "Manual", "cost": 25000, "deposit": 4000, "mileage": 12000, "age": 2, "rental_cost": 80, "image": "images/car2.jpeg"},
            {"name": "Renault Megan", "transmission": "Automatic", "cost": 35000, "deposit": 6000, "mileage": 8000, "age": 4, "rental_cost": 120, "image": "images/car3.jpeg"},
            {"name": "Opel Astra", "transmission": "Manual", "cost": 18000, "deposit": 2000, "mileage": 11000, "age": 5, "rental_cost": 75, "image": "images/car4.jpeg"},
            {"name": "Volkswagen Golf", "transmission": "Manual", "cost": 28000, "deposit": 5500, "mileage": 7000, "age": 1, "rental_cost": 110, "image": "images/car5.jpeg"},
            {"name": "BMW x5", "transmission": "Automatic", "cost": 22000, "deposit": 4700, "mileage": 15000, "age": 7, "rental_cost": 95, "image": "images/car6.jpeg"},
            {"name": "Suzuki Swift", "transmission": "Manual", "cost": 37000, "deposit": 4600, "mileage": 8400, "age": 6, "rental_cost": 89, "image": "images/car7.jpeg"},
            {"name": "Mazda cx5", "transmission": "Manual", "cost": 48000, "deposit": 5200, "mileage": 34000, "age": 4, "rental_cost": 56, "image": "images/car8.jpeg"},
            {"name": "Porsche Cayenne", "transmission": "Automatic", "cost": 95000, "deposit": 12000, "mileage": 34000, "age": 2, "rental_cost": 95, "image": "images/car9.jpeg"},
            {"name": "Volkswagen Beetle", "transmission": "Automatic", "cost": 78000, "deposit": 9500, "mileage": 23000, "age": 5, "rental_cost": 76, "image": "images/car10.jpeg"},
        ]

        car_index = 0
        for office in offices:
            for _ in range(2):
                car = Car(**car_data[car_index], office_id=office.id)
                db.session.add(car)
                car_index += 1
        db.session.commit()

        print("Sample data created successfully.")

@app.before_request
def set_language():
    session.setdefault("language", "en")

@app.context_processor
def inject_language():
    lang = session.get("language", "en")
    return dict(language=lang, translations=LANGUAGES[lang])

@app.route("/set_language/<lang>")
def set_language_route(lang):
    if lang in LANGUAGES:
        session["language"] = lang
    return redirect(request.referrer or url_for("home"))

from flask import Flask, render_template, request, session, jsonify
from models.models import db, Office

@app.route('/')
def home():
    user_city = request.args.get('city')  # Kullanıcının şehrini almak için
    if user_city:
        offices = Office.query.filter_by(location=user_city).all()
    else:
        offices = Office.query.all()  # Eğer şehir bilinmiyorsa tüm ofisleri göster
    
    locations = [{"id": office.id, "lat": office.latitude, "lng": office.longitude, "name": office.name} for office in offices]

    return render_template('home.html', offices=offices, locations=locations)

@app.route('/get_location', methods=['POST'])
def get_location():
    data = request.json
    user_city = data.get("city")
    session["user_city"] = user_city
    return jsonify({"success": True, "city": user_city})


@app.route('/search')
def search():
    pickup_office_id = request.args.get('pickup_office')
    pickup_date = request.args.get('pickup_date')
    pickup_time = request.args.get('pickup_time')
    return_office_id = request.args.get('return_office')
    return_date = request.args.get('return_date')
    return_time = request.args.get('return_time')
    
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'asc')  
    filter_transmission = request.args.get('filter_transmission')
    
    cars_query = Car.query.filter_by(office_id=pickup_office_id)

    if filter_transmission:
        cars_query = cars_query.filter_by(transmission=filter_transmission)
    
    if sort_by:
        if sort_by == 'cost':
            cars_query = cars_query.order_by(Car.cost.asc() if sort_order == 'asc' else Car.cost.desc())
        elif sort_by == 'mileage':
            cars_query = cars_query.order_by(Car.mileage.asc() if sort_order == 'asc' else Car.mileage.desc())
        elif sort_by == 'age':
            cars_query = cars_query.order_by(Car.age.asc() if sort_order == 'asc' else Car.age.desc())
        elif sort_by == 'rental_cost':
            cars_query = cars_query.order_by(Car.rental_cost.asc() if sort_order == 'asc' else Car.rental_cost.desc())
        else:  
            cars_query = cars_query.order_by(Car.transmission.asc() if sort_order == 'asc' else Car.transmission.desc())

    cars = cars_query.all()

    return render_template('search_results.html', cars=cars)


@app.route('/offices')
def show_offices():
    offices = Office.query.all()  # Veritabanından ofisleri çek
    return render_template('officeinfo.html', offices=offices)


@app.route('/office/<int:office_id>')
def office_info(office_id):
    office = Office.query.get_or_404(office_id)
    return render_template('office_info.html', office=office)

@app.route('/office/<int:office_id>/cars')
def show_office_cars(office_id):
    office = Office.query.get_or_404(office_id)
    return render_template('search_results.html', cars=office.cars)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username  
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        country = request.form['country']
        city = request.form['city']
        profile_picture = request.files.get('profile_picture')

        new_user = User(email=email, username=username, password=hash_password(password),country=country, city=city)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True)
