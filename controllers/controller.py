from flask import Flask, render_template, redirect, request, url_for
from flask import current_app as app
from flask_login import login_user, login_required, login_manager, current_user

from .models import *
this_user=None
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


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    lots = ParkingLot.query.all() 
    return render_template("admin_home.html", lots=lots, user=current_user)

@app.route("/user_dashboard")
@login_required
def user_dashboard():
    lots = ParkingLot.query.all()
    lots_avl = []

    for lot in lots:
        total_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").count()
        lots_avl.append({
            "lot": lot,
            "available": available_spots,
            "total": total_spots
        })

    return render_template("user_home.html", lots=lots_avl, user=current_user)

@app.route("/add_lot", methods=["GET", "POST"])
@login_required
def add_lot():
    if request.method == "POST":
        location = request.form.get("location")
        address = request.form.get("address")
        price = request.form.get("price")
        max_spots = request.form.get("max_spots")
        pincode = request.form.get("pincode")
        
        new_lot = ParkingLot(prime_location_name=location, address=address, price=price,
        pincode=pincode, maximum_spots=max_spots)
        db.session.add(new_lot)
        db.session.commit()

        for _ in range(new_lot.maximum_spots):
            spot = ParkingSpot(lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()

        return redirect("/admin_dashboard")
        return render_template("admin_home.html",user=this_user)
            
    return render_template("new_lot.html")

@app.route("/book_spot/<int:lot_id>", methods=["GET", "POST"])
@login_required
def book_spot(lot_id):
    this_lot = ParkingLot.query.filter_by(id=lot_id).first()
    avl_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first()
    if request.method == "POST":
        v_no = request.form.get("vehicle_no")
        
        new_reservation = Reservation(
            spot_id=avl_spot.id, user_id=current_user.id,
            lot_id=this_lot.price, parking_price=this_lot.price, 
            vehicle_no=v_no)
        db.session.add(new_reservation)
        avl_spot.status = 'O'
        db.session.commit()

        return redirect("/user_dashboard")

    return render_template("book_spot.html",lot=this_lot, user=current_user, spot=avl_spot)

@app.route("/edit_lot/<int:lot_id>", methods=["GET", "POST"])
@login_required
def edit_lot(lot_id):
    if request.method == "POST":
        this_lot.prime_location_name = request.form.get("location")
        this_lot.address = request.form.get("address")
        this_lot.price = float(request.form.get("price"))
        this_lot.pincode = request.form.get("pincode")
        existing_spots = this_lot.maximum_spots

        max_spots = int(request.form.get("max_spots"))
        if existing_spots == max_spots:
            pass
        elif existing_spots < max_spots:
            for _ in range(max_spots-existing_spots):
                spot = ParkingSpot(lot_id=this_lot.id)
                db.session.add(spot)
        else:
            excess = existing_spots - this_lot.maximum_spots
            available_spots = ParkingSpot.query.filter_by(lot_id=this_lot.id, status='A').limit(excess).all()

            if len(available_spots) < excess:
                flash("Cannot reduce spots. Too many are currently occupied.", "danger")
                return redirect("/edit_lot/{}".format(this_lot.id))

            for spot in available_spots:
                db.session.delete(spot)

        db.session.commit()
        return redirect("/admin_dashboard")

    this_lot = ParkingLot.query.filter_by(id=lot_id).first()
    return render_template("edit_lot.html",lot=this_lot)