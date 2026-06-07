from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# Reservation Model
# ==========================

class Reservation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    date = db.Column(db.String(50))
    time = db.Column(db.String(50))

    guests = db.Column(db.Integer)


# ==========================
# User Model
# ==========================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    phone = db.Column(db.String(20))
    city = db.Column(db.String(100))

    password = db.Column(db.String(255))


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# About Page
# ==========================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================
# Menu Page
# ==========================

@app.route("/menu")
def menu():
    return render_template("menu.html")


# ==========================
# Contact Page
# ==========================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ==========================
# Gallery Page
# ==========================

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# ==========================
# Chefs Page
# ==========================

@app.route("/chefs")
def chefs():
    return render_template("chefs.html")


# ==========================
# Login Page
# ==========================

@app.route("/login")
def login():
    return render_template("login.html")


# ==========================
# Register Page
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        city = request.form["city"]

        password = generate_password_hash(
            request.form["password"]
        )

        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            city=city,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ==========================
# Booking Page
# ==========================

@app.route("/booking", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        reservation = Reservation(
            name=request.form["name"],
            email=request.form["email"],
            date=request.form["date"],
            time=request.form["time"],
            guests=request.form["guests"]
        )

        db.session.add(reservation)
        db.session.commit()

    return render_template("booking.html")


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    reservations = Reservation.query.all()

    return render_template(
        "dashboard.html",
        reservations=reservations
    )
@app.route("/tables")
def tables():
    return render_template("tables.html", reservations=Reservation.query.all())


# ==========================
# Run App
# ==========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)