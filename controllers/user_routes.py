from flask import Flask, render_template, redirect, request, url_for
from flask import current_app as app
from flask_login import login_user, login_required, login_manager, current_user, logout_user

from sqlalchemy import or_, and_, func

from datetime import datetime, timedelta
import pytz
ist = pytz.timezone("Asia/Kolkata")

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
fig, ax = plt.subplots(figsize=(6, 4))
colors = ["tab:red", "tab:blue", "tab:green","tab:orange", "tab:purple", "tab:brown", "gold","lawngreen"]


from .models import *

@app.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    lots = ParkingLot.query.filter_by(active=1)
    lots_avl = []
    keyword = ""

    if request.method == "POST":
        kword = request.form.get("keyword")
        lots = ParkingLot.query.filter(
            ParkingLot.prime_location_name.ilike(f"%{kword}%") |
            ParkingLot.address.ilike(f"%{kword}%") |
            ParkingLot.pincode.ilike(f"%{kword}%")
        ).all()

    for lot in lots:
        total_spots = ParkingSpot.query.filter_by(lot_id=lot.id, active=1).count()
        avl_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").count()
        lots_avl.append({
            "lot": lot,
            "available": avl_spots,
            "total": total_spots
        })
    reservations = Reservation.query.filter_by(user_id=current_user.id)
    parking_history = []
    for event in reservations:
        lot = ParkingLot.query.filter_by(id=event.lot_id).first()
        duration='Not yet released'
        cost = "--"
        if event.cost:
            cost=f"Rs.{event.cost}"
        if event.leaving_timestamp!=None:
            total_minutes = int((event.leaving_timestamp - event.parking_timestamp).total_seconds() / 60)
            duration = "{} hrs and {} min".format(total_minutes//60, total_minutes%60 )
        parking_history.append({"booking": event, "lot": lot, "duration": duration, "cost": cost })
    return render_template("user_home.html", lots=lots_avl, user=current_user, history=parking_history)

@app.route('/summary')
def user_summary():
    bookings = Reservation.query.filter(Reservation.user_id==current_user.id, Reservation.leaving_timestamp!=None)
    count = bookings.count()
    total_duration_in_sec = sum( [ (i.leaving_timestamp-i.parking_timestamp).total_seconds() for i in bookings ])
    total_minutes = int(total_duration_in_sec//60)
    duration = "{} hr & {} min".format(total_minutes//60, total_minutes%60 )

    total_cost = sum([i.cost for i in bookings ])


    used_lots = db.session.query(Reservation.lot_id).filter(Reservation.user_id==current_user.id, Reservation.leaving_timestamp!=None)
    lots_dict = {}
    for (l_id,) in used_lots:
        lot = ParkingLot.query.filter_by(id=l_id).first()
        name = lot.prime_location_name.strip()
        if len(name)>12:
            name = name.replace(' ','\n')
        if name not in lots_dict:
            lots_dict[name] = 0
        lots_dict[name] += 1
    lots = list(lots_dict.keys())
    counts = list(lots_dict.values())
    n = len(lots_dict)
    ax.bar(lots, counts, color=colors[:n])
    ax.set_xlabel("Location")
    ax.set_ylabel("Usage frequency")
    fig.tight_layout()
    print(lots_dict, colors[:n],n)
    #plt.title("Parking distribution across Locations")
    fig.savefig(f"static/users_chart/bar_{current_user.id}.png")
    plt.close(fig)
    ax.clear()
    
    return render_template("user_summary.html", user=current_user, count=count,
     duration=duration, cost=total_cost)

@app.route("/book_spot/<int:lot_id>", methods=["GET", "POST"])
@login_required
def book_spot(lot_id):
    this_lot = ParkingLot.query.filter_by(id=lot_id).first()
    avl_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first()
    if request.method == "POST":
        v_no = request.form.get("vehicle_no")
        now = datetime.now(ist)
        new_reservation = Reservation(
            spot_id=avl_spot.id, user_id=current_user.id,
            lot_id=lot_id, parking_price=this_lot.price, 
            vehicle_no=v_no, parking_timestamp=now)
        db.session.add(new_reservation)
        avl_spot.status = 'O'
        db.session.commit()

        return redirect("/user_dashboard")

    return render_template("book_spot.html", lot=this_lot, user=current_user, spot=avl_spot)

@app.route("/release_spot/<int:booking_id>", methods=["GET", "POST"])
@login_required
def release_spot(booking_id):
    booking = Reservation.query.filter_by(id=booking_id).first()
    lot = ParkingLot.query.filter_by(id=booking.lot_id).first()
    now = datetime.now(ist)
    current_time = now.strftime("%H:%M") 
    start_time = ist.localize(booking.parking_timestamp)
    total_minutes = int((now - start_time).total_seconds() / 60)
    duration = "{} hour(s) and {} minute(s)".format(total_minutes//60, total_minutes%60 )
    cost = int(booking.parking_price * total_minutes / 60 )

    if request.method == "POST":
        
        booking.leaving_timestamp=now
        this_spot = ParkingSpot.query.filter_by(id=booking.spot_id).first()
        this_spot.status = 'A'
        booking.cost = cost
        db.session.commit()

        return redirect("/user_dashboard")

    return render_template("release_spot.html", booking=booking, 
        current_time=now, cost=cost, duration=duration )


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        this_user = User.query.filter_by(id=current_user.id).first()
        this_user.name = request.form.get("name")
        this_user.address = request.form.get("address")
        this_user.pincode = request.form.get("pincode")
        db.session.commit()
        if this_user.type == "admin":
            return redirect("/admin_dashboard")
        return redirect("/user_dashboard")
            
    return render_template("edit_profile.html",user=current_user)