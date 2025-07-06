from flask import Flask, render_template, redirect, request, url_for
from flask import current_app as app
from flask_login import login_user, login_required, login_manager, current_user
from datetime import datetime, timedelta
from sqlalchemy import or_, and_
import pytz
ist = pytz.timezone("Asia/Kolkata")

from .models import *

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
    lots = ParkingLot.query.filter_by(active=1) 
    lot_with_avl = []
    for lot in lots:
        tot = ParkingSpot.query.filter_by(lot_id=lot.id, active=1).count()
        occ = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        lot_with_avl.append({"info": lot, "total": tot, "occupied": occ})
    return render_template("admin_home.html", lots=lot_with_avl, user=current_user)

@app.route('/delete/<int:lot_id>')
def delete_lot(lot_id):
    ParkingLot.query.filter_by(id=lot_id).first().active = 0
    spots = ParkingSpot.query.filter_by(lot_id=lot_id)
    for spot in spots:
        spot.active=0
        spot.status='I'
    db.session.commit()
    return redirect("/admin_dashboard")
    

@app.route('/admin_dashboard/users')
@login_required
def admin_users():
    user_list = User.query.filter_by(type="general")
    return render_template("admin_users.html", user=current_user, list = user_list)

@app.route('/admin_dashboard/search', methods=["GET","POST"])
@login_required
def admin_search():
    if request.method == "POST":
        searchtype =request.form.get("type")
        kword=request.form.get("keyword")

        if searchtype=="1":
            user_list=User.query.filter(
                User.username.ilike(f"%{kword}%") |
                User.id.ilike(f"%{kword}%") |
                User.name.ilike(f"%{kword}%")
            ).all()
            return render_template("admin_search.html", user=current_user, users=user_list, keyword=kword)
        
        elif searchtype=="2":
            lots = ParkingLot.query.filter(
                ParkingLot.prime_location_name.ilike(f"%{kword}%") |
                ParkingLot.address.ilike(f"%{kword}%") |
                ParkingLot.pincode.ilike(f"%{kword}%")
            ).all()
            lots = ParkingLot.query.filter(
                and_(ParkingLot.active == 1,
                    or_(ParkingLot.prime_location_name.ilike(f"%{kword}%"),
                        ParkingLot.address.ilike(f"%{kword}%"),
                        ParkingLot.pincode.ilike(f"%{kword}%") ))).all()
            lot_with_avl = []
            for lot in lots:
                tot = ParkingSpot.query.filter_by(lot_id=lot.id, active=1).count()
                occ = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
                lot_with_avl.append({"info": lot, "total": tot, "occupied": occ})
            return render_template("admin_search.html", user=current_user, lots=lot_with_avl, keyword=kword)
    return render_template("admin_search.html", user=current_user)

@app.route('/user_details/<int:user_id>', methods=["GET","POST"])
def user_details(user_id):
    user=User.query.filter_by(id=user_id).first()
    reservations = Reservation.query.filter_by(user_id=user_id)
    parking_history = []
    for event in reservations:
        lot = ParkingLot.query.filter_by(id=event.lot_id).first()
        duration='Not yet released'
        if event.leaving_timestamp!=None:
            total_minutes = int((event.leaving_timestamp - event.parking_timestamp).total_seconds() / 60)
            duration = "{} hour(s) and {} minute(s)".format(total_minutes//60, total_minutes%60 )
        parking_history.append({"booking": event, "lot": lot, "duration": duration })

    if request.method == "POST":
        user.name=request.form.get("name")
        user.address=request.form.get("address")
        db.session.commit()
        return redirect(url_for("user_details", user_id=user.id))
    return render_template("user_details.html",user=user, history=parking_history)

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
        if event.leaving_timestamp!=None:
            total_minutes = int((event.leaving_timestamp - event.parking_timestamp).total_seconds() / 60)
            duration = "{} hour(s) and {} minute(s)".format(total_minutes//60, total_minutes%60 )
        parking_history.append({"booking": event, "lot": lot, "duration": duration })
    return render_template("user_home.html", lots=lots_avl, user=current_user, history=parking_history)

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
        
        new_id = new_lot.id*10000
        for num in range(new_lot.maximum_spots):
            new_id += 1
            spot = ParkingSpot(id=new_id, lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()

        return redirect("/admin_dashboard")
        return render_template("admin_home.html",user=this_user)
            
    return render_template("new_lot.html")

@app.route("/edit_lot/<int:lot_id>", methods=["GET", "POST"])
@login_required
def edit_lot(lot_id):
    this_lot = ParkingLot.query.filter_by(id=lot_id).first()
    if request.method == "POST":
        this_lot.prime_location_name = request.form.get("location")
        this_lot.address = request.form.get("address")
        this_lot.price = float(request.form.get("price"))
        this_lot.pincode = request.form.get("pincode")
        existing_spots = ParkingSpot.query.filter_by(lot_id=this_lot.id, active=1).count()

        max_spots = int(request.form.get("max_spots"))
        if existing_spots == max_spots:
            pass
        elif existing_spots < max_spots:
            print("Adding spots")
            last_id = ParkingSpot.query.filter_by(lot_id=lot_id).order_by(ParkingSpot.id.desc()).first().id
            for num in range(max_spots-existing_spots):
                last_id +=1
                spot = ParkingSpot(lot_id=this_lot.id, id=last_id)
                this_lot.maximum_spots = max_spots
                db.session.add(spot)
        else:
            print("Deleting spots")
            excess = existing_spots - max_spots
            available_spots = ParkingSpot.query.filter_by(lot_id=this_lot.id, status='A')\
                .order_by(ParkingSpot.id.desc()).limit(excess).all()

            if len(available_spots) < excess:
                return redirect(url_for("edit_lot", lot_id=this_lot.id))

            for spot in available_spots:
                spot.active = 0
                spot.status = 'I'
            this_lot.maximum_spots = max_spots

        db.session.commit()
        return redirect("/admin_dashboard")

    return render_template("edit_lot.html",lot=this_lot)

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

@app.route("/view_spot/<int:spot_id>", methods=["GET", "POST"])
@login_required
def view_spot(spot_id):
    this_spot = ParkingSpot.query.filter_by(id=spot_id).first()
    if request.method == "POST":
        this_lot = ParkingLot.query.filter_by(id=this_spot.lot_id).first()
        this_lot.maximum_spots -= 1
        this_spot.active = 0
        this_spot.status = 'I'

        db.session.commit()
        return redirect("/admin_dashboard")

    return render_template("view_spot.html", spot=this_spot)

@app.route("/spot_details/<int:spot_id>")
@login_required
def spot_details(spot_id):
    this_spot = ParkingSpot.query.filter_by(id=spot_id).first()
    booking = Reservation.query.filter_by(spot_id=spot_id, leaving_timestamp=None).first()
    customer = User.query.filter_by(id=booking.user_id).first()
    now = datetime.now(ist)
    start_time = ist.localize(booking.parking_timestamp)
    total_minutes = int((now - start_time).total_seconds() / 60)
    duration = "{} hour(s) and {} minute(s)".format(total_minutes//60, total_minutes%60 )
    
    cost = int(booking.parking_price * total_minutes / 60 )
    return render_template("spot_details.html", spot=this_spot, booking=booking, cost=cost, user=current_user, customer=customer)