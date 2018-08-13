"""Essentially app."""

# Included because we want jinja to fail loudly, otherwise failure will be unknown

from jinja2 import StrictUndefined

import os

import APIrequest_fcns

import bcrypt

from flask import Flask, render_template, redirect, request, flash, session
# from flask_debugtoolbar import DebugToolbarExtension

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

    return render_template('homepage.html')       

@app.route('/loginform', methods=['GET'])
def login_form():
    """Shows login form."""

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def store_login():
    """Requests and stores info from login form."""

    # VERIFY INFO FROM LOGIN AGAINST DB INFO STORED WHEN ACCT CREATED

@app.route('/createaccountform', methods=['GET'])
def account_form():
    """Shows the create account form."""

    return render_template('createacct.html', fname = '',
                                            lname = '',
                                            username = '',
                                            phone = '',
                                            email = '')

@app.route('/createaccount', methods=['POST'])
def store_created_account():
    """Requests and stores info from login form."""

    # STORE INFO FROM CREATE ACCT FORM IN DB

    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    phone = request.form['phone']
    email = request.form['email']

    # Confirm that passwords actually match
    if password == confirm:

        # Query the db, to ensure that the username is not taken
        check_username = User.query.filter(User.username == username).first()
        if check_username is None:
            continue
        else:
            flash('That username is already taken.')
            return render_template('creatacct.html', fname = fname,
                                                    lname = lname,
                                                    username = usernamee,
                                                    phone = phone,
                                                    email = email)

        # Query the db, to ensure that the email is not taken
        check_email = User.query.filter(User.email == email).first()
        if check_email is None:
            continue
        else: 
            flash('That email is already registered.')

        # Query the db, to ensure that the phone number is not taken
        check_phone = User.query.filter(User.phone == phone).first()
        if check_phone is None:
            continue
        else: 
            flash('That phone number is already attached to an account.')
        
        if check_username is None and check_email is None and check_phone is None:
            new_user = User(fname = fname,
                            lname = lname,
                            username = username,
                            phone = phone,
                            email = email)

            db.session.add(new_user)
            db.session.commit()

            print(new_user.user_id)

            # Hash password, then store
            password = b + password
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
            new_user_password = Password(user_id = new_user.user_id,
                                        hash_pass = hashed_password)

            db.session.add(new_user_password)
            db.session.commit()

        # make call to finicity before creating new user, then create new user all at once
    else:
        flash('Looks like your passwords don\'t match. That\'s essential.')

        #     data = {'location.address' : location,
        #     'location.within' : distance,
        #     'sort_by' : sort,
        #     'token' : os.environ['EVENTBRITE_TOKEN']}
        
        # r = requests.get("https://www.eventbrite.com/v3/events/search", params=data)

@app.route('/forgotpassword', methods=['GET'])
def forogt_password():
    """Shows login form."""

    return render_template('forgotpassword.html')

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

    # Show detailed information on page where you add institutions?

@app.route('/logout')
def logout():
    """Allows the user to log out, ends the session."""

    # Add logout button on all pages except home page
    # Event listener, when button is clicked, end session?


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
