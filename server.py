"""Essentially app."""

# Included because we want jinja to fail loudly, otherwise failure will be unknown

from jinja2 import StrictUndefined

import os

import APIrequest_fcns

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

    render_template(homepage.html)

    if (EVENT LISTENER FOR LOGIN FORM)
        return redirect('/loginform')
    if (EVEN LISTENER FOR CREAT ACCT)
        return redirect('/createaccountform')

@app.route('/loginform')
def login_form():
    """Shows login form."""

    return render_template(login.html)

@app.route('/login')
def store_login():
    """Requests and stores info from login form."""

    VERIFY INFO FROM LOGIN AGAINST DB INFO STORED WHEN ACCT CREATED

@app.route('/createaccountform')
def account_form():
    """Shows the create account form."""

    return render_template(createaccount.html)

@app.route('/createaccount')
def store_created_account():
    """Requests and stores info from login form."""

    STORE INFO FROM CREATE ACCT FORM IN DB 

@app.route('/addinstitution')
def add_institution():
    """Allows users to search for and associate an institution with their profile."""

@app.route('/addaccounts')
def add_accounts():
    """Allows users to select and add accounts from their chosen institution."""

@app.route('/sorttransactions')
def sort_transactions():
    """Allows users to categorize transactions as essential or non-essential."""

@app.route('/essentialvisual')
def display_essential_visual():
    """Displays the primary data visual."""

@app.route('/institutioninfo')
def display_institution_info():
    """Displays detailed information about a selected institution."""

@app.route('/logout')
def logout():
    """Allows the user to log out, ends the session."""



