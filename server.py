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

    username = request.form['username'] 
    password = request.form['password']

    # Lowercase username to check against db
    low_username = username.lower()

    # Check if the username entered is already int he db
    user_in_db = User.query.filter(User.username == low_username).first()

    if user_in_db is None:
        flash('Your credentials are incorrect, or you need to make an account.')
        return redirect('/loginform')

    elif user_in_db is not None:
        # Get the user_id of the user that was found in the above query
        user_id = user_in_db.user_id
        print(user_id)

        # Get the hashed password of the user that was found in the above query
        # passwords[0] needed because of the way SQL Alchemy returns the info
        # i.e., if the user had multiple passwords, they would be returned in a list,
        # and we would want the first one in that list, so that is how we need to 
        # index it right now
        user_password = user_in_db.passwords[0].hash_pass

        if user_in_db.username == low_username and bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
            # print('Yay! Matching hashes!')
            session['user_id'] = user_id
            # print('I saved this person to the session for you!')
            return redirect('/sorttransactions')


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
    # Understood via regex101.com
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

    # Format username so that all usernames are stored in lowercase only
    low_username = username.lower()
    # print(low_username)


    # Confirm that passwords actually match
    if password == confirm:

        # Query the db, to ensure that the username is not taken
        check_username = User.query.filter(User.username == low_username).first()
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
            flash('That username is already taken.')
            return render_template('createacct.html', fname = fname,
                                                    lname = lname,
                                                    username = '',
                                                    phone = phone,
                                                    email = email)

        # Query the db, to ensure that the email is not taken
        check_email = User.query.filter(User.email == email).first()
        if check_email is not None:
            flash('That email is already registered.')
            return render_template('createacct.html', fname = fname,
                                                    lname = lname,
                                                    username = username,
                                                    phone = phone,
                                                    email = '')

        # Query the db, to ensure that the phone number is not taken
        check_phone = User.query.filter(User.phone == f_phone).first()
        if check_phone is not None:           
            flash('That phone number is already attached to an account.')
            return render_template('createacct.html', fname = fname,
                                                    lname = lname,
                                                    username = username,
                                                    phone = phone,
                                                    email = email)
        
        if check_username is None and check_email is None and check_phone is None:

            # Make call to Finicity, to get fin_id, createdDate before creating user
            new_customer = AddTestingCustomer(low_username, fname, lname)
            
            new_customer_id = new_customer['id']
            new_customer_date = new_customer['createdDate']

            # Add new user to db
            new_user = User(fin_id = new_customer_id,
                            created_date = new_customer_date,
                            fname = fname,
                            lname = lname,
                            username = low_username,
                            phone = f_phone,
                            email = email)

            db.session.add(new_user)
            db.session.commit()

            # Save fin_id to session for use in AddAccounts
            session['fin_id'] = new_customer_id

            # print(new_user.user_id)

            # Hash password, then store
            b = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
        
            new_user_password = Password(user_id = new_user.user_id,
                                        hash_pass = hashed_password.decode('utf-8'))

            db.session.add(new_user_password)
            db.session.commit()

    else:
        flash('Looks like your passwords don\'t match. That\'s essential.')


    return render_template('addinstitution.html')


@app.route('/forgotpassword', methods=['GET'])
def forgot_password():
    """Shows login form."""
    
    #TODO MUCH LATER 
    return render_template('forgotpassword.html')  


@app.route('/addinstitution')
def add_institution():
    """Allows users to search for and associate an institution with their profile."""

    # TODO 
    return render_template('addinstitution.html')


@app.route('/showinstitutions', methods=['GET'])
def show_institutions():
    """Displays results of user's institution search."""

    bank_choice = request.args.get('bank_choice')
    # print("Got the bank!")

    # Save bank id number to session, shouldn't need after initial setup
    session['bank_choice'] = bank_choice

    bank_choices = GetInstitutions(bank_choice)
    num_banks = int(bank_choices['found'])

    # print(bank_choices['institutions'])
    # print(bank_choices['institutions'][0])
    # print(bank_choices['institutions'][0]['id'])
    # print(institution_dict)



    # then discover customer accounts, get historic transactions, and refresh accounts at same time
    # Use get Transaction details to display transactions to user
    # Let user select transactions, categorize, add categorizations to db
    # Use db to display info in donut chart

    return render_template('showinstitutions.html', 
                            bank_choices=bank_choices, 
                            num_banks = num_banks)


@app.route('/institutionloginform', methods=['GET'])
def institution_login():
    """Gets bank_id from the bank selected by the user, and generates the correct 
        login form. Add in detail in later version."""

    bank_id = request.args.get('select_bank')
    GetInstitutionLogin(bank_id)
    # BUILD OUT POST-HACKBRIGHT

    return render_template('institutionlogin.html')

@app.route('/institutionlogin', methods=['POST'])
def institution_form():
    """Allows users to login to their bank--REQUIRES OAUTH for actual banks. 
        Build out in later version."""

    banking_userid = request.form['banking_userid']
    banking_password = request.form['banking_password']
    # print(banking_userid)
    # print(banking_password)

    # Save banking_userid and banking_password to session, to add accounts
    session['banking_userid'] = banking_userid
    session['banking_password'] = banking_password

    return render_template('permission.html')


@app.route('/addaccounts')
def add_accounts():
    """Allows users to select and add accounts from their chosen institution."""

    permission = request.args.get('permission')

    if permission == 'yes':
        # print('YAY')
    else: 
        flash('Are you sure? You cannot use essentially if you choose "Nope."')
        return render_template('permission.html')


    customerId = session.get('fin_id')
    institutionId = session.get('bank_choice')
    banking_userid = session.get('banking_userid')
    banking_password = session.get('banking_password')

    DiscoverCustomerAccounts(customerId, institutionId, banking_userid, banking_password)
    # Should I add a UserData table instead?
   
    return render_template('showaccounts.html')


@app.route('/showaccounts')
def show_accounts():
    """Displays results of account discovery for a particular customer/institution."""

# @app.route('/sorttransactions')
# def sort_transactions():
#     """Allows users to categorize transactions as essential or non-essential."""

    # return render_template('homepage.html') 
    #TODO, TEMPORARY REDIRECT FOR NOW



# @app.route('/essentialvisual')
# def display_essential_visual():
#     """Displays the primary data visual."""

    #TODO 

# @app.route('/institutioninfo')
# def display_institution_info():
#     """Displays detailed information about a selected institution."""

#     # Show detailed information on page where you add institutions?
    #TODO 


@app.route('/logout')
def logout():
    """Allows the user to log out, ends the session."""

    del session['user_id']
    # methods to delete the whole session
    return redirect('/login')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
