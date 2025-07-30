from flask import Flask
from controllers.database import db
from flask_login import LoginManager
app = None

# use this to create database and kickstart myapp  
# from app import *
# db.create_all()

def create_app():
    app = Flask(__name__)
    app.secret_key = "mysecretkey"
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///vehicleparkingapp.sqlite3" #database is created
    db.init_app(app)
    app.app_context().push() #runtime error, brings everything under context of flask app
    return app

app = create_app()
from controllers.controller import * 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
    #return User.query.get(int(user_id)) old one; but no errors
    
    
if __name__ == "__main__":
    app.run(debug = True)