"""Essentially app."""

# Included because we want jinja to fail loudly, otherwise failure will be unknown

from jinja2 import StrictUndefined

import os

from flask import Flask, render_template, redirect, request, flash session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Transaction, Transact_Category, Password, Security

# What does this do?
from warnings import warn


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

@app.route('/loginform')
def login_form():
    """Shows login form."""

@app.route('/login')
def 

@app.route('/sorttransactions')
def 

@app.route('/essentialvisual')
def 

@app.route('/createaccountform')
def 

@app.route('/createaccount')
def 

@app.route('/createfinaccountform')
def 

@app.route('/createfinaccount')
def 

@app.route('/addinstitution')
def 

@app.route('/addaccounts')
def 

@app.route('/institutioninfo')
def 

@app.route('/logout')
def 



