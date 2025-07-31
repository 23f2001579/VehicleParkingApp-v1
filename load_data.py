import csv
from app import db
from controllers.models import *

with open('sample_data/users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user = User(id=row['id'], username=row['username'], name=row['name'],
            password=row['password'], type=row['type'], address=row['address'],  pincode=row['pincode'])
        db.session.add(user)
    db.session.commit()

with open('sample_data/lots.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        lot = ParkingLot(id=row['id'], prime_location_name=row['prime_location_name'], price=row['price'],
            address=row['address'], maximum_spots=row['maximum_spots'], pincode=row['pincode'], active=bool(row["active"]))
        db.session.add(lot)
    db.session.commit()

with open('sample_data/spots.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        spot = ParkingSpot(id=row['id'], lot_id=row['lot_id'], status=row['status'],
            active=bool(row["active"]))
        db.session.add(spot)
    db.session.commit()


