from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(50))
    name = db.Column(db.String(100))
    generic_name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    form = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    selling_price = db.Column(db.Float)
    expiry_date = db.Column(db.String(20))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_code = db.Column(db.String(50))
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    password = db.Column(db.String(100))

    role = db.Column(db.String(50))
    department = db.Column(db.String(100))

    status = db.Column(db.String(50))

    last_login = db.Column(db.String(50))