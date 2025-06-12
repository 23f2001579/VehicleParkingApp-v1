from flask import Flask, render_template, redirect, request 
from flask import current_app as app

from .models import *

@app.route("/login", methods=["GET", "POST"]) #url with specific http method gives specific
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    return render_template("admin_home.html",user=this_user)
                else:
                    return render_template("user_home.html",user=this_user)
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

