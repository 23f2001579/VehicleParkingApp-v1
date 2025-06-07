from flask import Flask
from controllers.database import db
app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///vehicleparkingapp.sqlite3"#3 database
    db.init_app(app)#3 database
    app.app_context().push() #runtime error, brings everything under context of flask applic
    return app

app = create_app()
from controllers.controllers import * #2 controllers
# from application.models import #indirect connection using controllers.py
if __name__ == "__main__":
    app.run(debug = True)