"""Essentially app."""

# Included because we want jinja to fail loudly, otherwise failure will be unknown

from jinja2 import StrictUndefined

import os

import re

import pdb

from APIrequest_fcns import *

import bcrypt

from flask import Flask, render_template, redirect, request, flash, session
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

    # Need to pass in empty strings so that the jinja doesn't get confused
    return render_template('createacct.html', fname = '',
                                            lname = '',
                                            username = '',
                                            phone = '',
                                            email = '')

@app.route('/createaccount', methods=['POST'])
def store_created_account():
    """Requests and stores info from login form."""

    # Get info from the create account form
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username'] 
    password = request.form['password']
    confirm = request.form['confirm']
    phone = request.form['phone']
    email = request.form['email']

    # print(email)


    # Confirm that email entered is valid
    match_obj = re.search(r'(\w+)\@(\w+)\.(\w+)', email)
    # print(match_obj)

    if match_obj is None:
        flash('That\'s not a valid email address.')
        return render_template('createacct.html', fname = fname,
                                                lname = lname,
                                                username = username,
                                                phone = phone,
                                                email = '')

    # Confirm that password entered contains at least 1 digit and 1 special character
    # https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
    match_obj = re.search("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]", password)

    if match_obj is None: 
        flash('Invalid password--try again!')
        return render_template('createacct.html', fname = fname,
                                                lname = lname,
                                                username = username,
                                                phone = phone,
                                                email = email)  

    # Format phone number for later use with Twilio, and so all numbers are stored identically
    phone_digits = ''.join(d for d in phone if d.isdigit())

    f_phone = "+1" + phone_digits 


    # Confirm that passwords actually match
    if password == confirm:

        # Query the db, to ensure that the username is not taken
        check_username = User.query.filter(User.username == username).first()
        if check_username is None:
            # Check to make sure the username is >= 8 characters long
            if len(username) < 8:
                flash('Your username must be at least 8 characters.')
                return render_template('createacct.html', fname = fname,
                                                        lname = lname,
                                                        username = '',
                                                        phone = phone,
                                                        email = email)

        else:
            # Do I need this flash message? How to display it?
            flash('That username is already taken.')
            return render_template('createacct.html', fname = fname,
                                                    lname = lname,
                                                    username = '',
                                                    phone = phone,
                                                    email = email)

        # Query the db, to ensure that the email is not taken
        check_email = User.query.filter(User.email == email).first()
        if check_email is not None:
            # Do I need this flash message? How to display it?
            flash('That email is already registered.')
            return render_template('createacct.html', fname = fname,
                                                    lname = lname,
                                                    username = username,
                                                    phone = phone,
                                                    email = '')

        # Query the db, to ensure that the phone number is not taken
        check_phone = User.query.filter(User.phone == f_phone).first()
        if check_phone is not None:
            # Do I need this flash message? How to display it?            
            flash('That phone number is already attached to an account.')
            return render_template('createacct.html', fname = fname,
                                                    lname = lname,
                                                    username = usernamee,
                                                    phone = phone,
                                                    email = email)
        
        if check_username is None and check_email is None and check_phone is None:

            # Make call to Finicity, to get fin_id, createdDate before creating user
            new_customer = AddTestingCustomer(username, fname, lname)
            
            new_customer_id = new_customer['id']
            new_customer_date = new_customer['createdDate']

            # Add new user to db
            new_user = User(fin_id = new_customer_id,
                            created_date = new_customer_date,
                            fname = fname,
                            lname = lname,
                            username = username,
                            phone = f_phone,
                            email = email)

            db.session.add(new_user)
            db.session.commit()

            # print(new_user.user_id)

            # Hash password, then store
            b = password.encode()
            hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
        
            new_user_password = Password(user_id = new_user.user_id,
                                        hash_pass = hashed_password)

            db.session.add(new_user_password)
            db.session.commit()

    else:
        flash('Looks like your passwords don\'t match. That\'s essential.')

        # REDIRECT SOMEWHERE

        #     data = {'location.address' : location,
        #     'location.within' : distance,
        #     'sort_by' : sort,
        #     'token' : os.environ['EVENTBRITE_TOKEN']}
        
        # r = requests.get("https://www.eventbrite.com/v3/events/search", params=data)
    return redirect("/loginform")

@app.route('/forgotpassword', methods=['GET'])
def forgot_password():
    """Shows login form."""

    return render_template('forgotpassword.html')

# @app.route('/addinstitution')
# def add_institution():
#     """Allows users to search for and associate an institution with their profile."""

# @app.route('/addaccounts')
# def add_accounts():
#     """Allows users to select and add accounts from their chosen institution."""

# @app.route('/sorttransactions')
# def sort_transactions():
#     """Allows users to categorize transactions as essential or non-essential."""

# USE SESSIONS TO KEEP TRANSACTIONS NON PUBLIC

# @app.route('/essentialvisual')
# def display_essential_visual():
#     """Displays the primary data visual."""

# @app.route('/institutioninfo')
# def display_institution_info():
#     """Displays detailed information about a selected institution."""

#     # Show detailed information on page where you add institutions?

# @app.route('/logout')
# def logout():
#     """Allows the user to log out, ends the session."""

#     # Add logout button on all pages except home page
#     # Event listener, when button is clicked, end session?
#     # Get help with logout process


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
