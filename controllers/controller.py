from flask import Flask, render_template, redirect, request, url_for
from flask import current_app as app
from flask_login import login_user, login_required, login_manager, current_user, logout_user

from sqlalchemy import or_, and_, func

from datetime import datetime, timedelta
import pytz
ist = pytz.timezone("Asia/Kolkata")

import matplotlib
import matplotlib.pyplot as plt
from controllers.admin_routes import *
matplotlib.use("Agg")
fig, ax = plt.subplots(figsize=(6, 4))
colors = ["tab:red", "tab:blue", "tab:green","tab:orange", "tab:purple", "tab:brown", "gold","lawngreen"]

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"]) #url with specific http method gives specific
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        global this_user
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == pwd:
                login_user(this_user)
                if this_user.type == "admin":
                    return redirect("/admin_dashboard")
                else:
                    return redirect("/user_dashboard")
            return "Incorrect password"
        return "Invalid user"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"]) #url with specific http method gives specific
def register():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        name = request.form.get("name")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        new_user = User.query.filter_by(username=username).first()
        if new_user:
            return "Email already in use"
        else:
            new_user = User(username=username, password=pwd, name=name, address=address, 
            pincode=pincode)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
            
    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


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