from controllers.admin_routes import *
from controllers.user_routes import *

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
    return render_template("auth/login.html")

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
            
    return render_template("auth/register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")