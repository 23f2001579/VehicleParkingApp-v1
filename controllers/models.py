from .database import db #check for this file in the folder you are existing
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable = False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    type = db.Column(db.String, default="general")
    pincode = db.Column(db.String(6), nullable=False)
    reservations = db.relationship('Reservation', backref='user')

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prime_location_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer,nullable = False)
    maximum_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot')

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')
    reservations = db.relationship('Reservation', backref='spot')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable = False)
    parking_timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    leaving_timestamp = db.Column(db.DateTime(timezone=True), nullable=True)
    parking_price = db.Column(db.Integer, nullable=False)
    vehicle_no = db.Column(db.String, nullable=False)

