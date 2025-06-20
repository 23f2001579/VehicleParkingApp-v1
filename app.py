from flask import Flask
from controllers.database import db
from flask_login import LoginManager
app = None

def create_app():
    app = Flask(__name__)
    app.secret_key = "mysecretkey"
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///vehicleparkingapp.sqlite3"#3 database
    db.init_app(app)#3 database
    app.app_context().push() #runtime error, brings everything under context of flask applic
    return app

app = create_app()
from controllers.controller import * #2 controllers
# from application.models import #indirect connection using controllers.py

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # name of your login route

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    
if __name__ == "__main__":
    app.run(debug = True)