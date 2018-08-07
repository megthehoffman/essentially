"""Models for essentially db."""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask 

# Could bind the instance of the db to a very specific Flask application, as such:
# app = Flask(__name__)
# db = SQLAlchemy(app)

# OR, could create the app one time and cofigure the application later to support it
# The difference between the two is that in the first case methods like create_all() 
# and drop_all() will work all the time but in the second case a 
# flask.Flask.app_context() has to exist--i.e. requires helper fcns (src: Flask docs)

db = SQLAlchemy()

# MODEL DEFS

# HELPER FCNS

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

