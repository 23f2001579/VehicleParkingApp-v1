from flask import Flask, render_template, redirect, request 
from flask import current_app as app

from .models import *

@app.route("/login", methods=["GET", "POST"]) #url with specific http method gives specific
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == pwd:
                if user.type == "admin":
                    return render_template("admin_home.html",username=username)
                else:
                    return render_template("user_home.html",user=user)
            return "Incorrect password"
        return "Invalid user"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"]) #url with specific http method gives specific
def register():
    if request.method == "POST":
        return "registered successfully"
    return render_template("register.html")