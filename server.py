"""Essentially app."""

# Included because we want jinja to fail loudly, otherwise failure will be unknown
from jinja2 import StrictUndefined
import os
import re
import pdb
from APIrequest_fcns import *
import bcrypt
import time
import random
from flask import Flask, render_template, redirect, request, flash, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from functools import wraps
from model import connect_to_db, db, User, Transaction, Transact_Category, Password, Security, UserBankAccount


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')       


@app.route('/loginform', methods=['GET'])
def display_login_form():
    """Shows login form."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def store_login_info():
    """Requests and stores info from login form."""

    # Get username and password from the HTML form
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
        # print(user_id)

        # Get the hashed password of the user that was found in the above query
        # passwords[0] needed because of the way SQL Alchemy returns the info
        # i.e., if the user had multiple passwords, they would be returned in a list,
        # and we would want the first one in that list, so that is how we need to 
        # index it right now
        user_password = user_in_db.passwords[0].hash_pass

        if user_in_db.username == low_username and bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
            # print('Yay! Matching hashes!')
            
            # Saves user_id in session ONLY after Login (not after Create Account)
            session['user_id'] = user_id

            # Use this user_id to query for a user in the db
            # SELECT customerId FROM users WHERE user_id == user_id 
            user = User.query.filter(User.user_id == user_id).first()

            # Set customerId = to the fin_id (customerId) for that user
            customerId = user.fin_id
            session['fin_id'] = customerId
                # print('I saved this person to the session for you!')

            new_transactions = get_transactions()
            # print(new_transactions)

            have_transactions = query_for_unsorted_transactions(session.get('user_id'))
            # print(have_transactions)

            if have_transactions is not None:
                return redirect('/showunsortedtransactions')
            else: 
                flash('You don\'t currently have any new transactions to sort!')
                return redirect('/essentialvisual')


@app.before_request
def load_user():
    """Assign g.user for use in login_required fcn."""
    if session.get('user_id'):
        # print(session.get('user_id'))
        g.user = session.get('user_id')
    else:
       g.user = None


# Helper fcn to make certain routes viewable only if logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('display_login_form', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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
            
            # Store these in variables for storage in db later
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

            # Commit to db session (NOT Flask session)
            db.session.add(new_user)
            db.session.commit()

            # Save fin_id to session for use in AddAccounts
            session['fin_id'] = new_customer_id

            # print(new_user.user_id)

            # Hash password, then store
            b = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
        
            # Add password for new user in db
            new_user_password = Password(user_id = new_user.user_id,
                                        hash_pass = hashed_password.decode('utf-8'))

            db.session.add(new_user_password)
            db.session.commit()

            # Saves user_id in session, ONLY after Create Account (not after Login)
            session['user_id'] = new_user.user_id

    else:
        flash('Looks like your passwords don\'t match. That\'s essential.')


    return render_template('addinstitution.html')


# @app.route('/showcreateaccountform', methods=['GET'])
# def show_create_acct_form():
#     """Shows completed Create Account form if user wants to make changes."""
    
#     # TODO MUCH LATER 
#     return render_template('')


@app.route('/forgotpassword', methods=['GET'])
def forgot_password():
    """Shows Forgot Password page."""
    
    # TODO MUCH LATER 
    return render_template('forgotpassword.html')  


@app.route('/addinstitution')
@login_required
def add_institution():
    """Allows users to search for and associate an institution with their profile."""

    return render_template('addinstitution.html')


@app.route('/showinstitutions', methods=['GET'])
@login_required
def show_institutions():
    """Displays results of user's institution search."""

    # Get user's single bank choice from dropdown
    bank_choice = request.args.get('bank_choice')
    # print("Got the bank!")

    # Uses dropdown value to GetInstitutions and counts the number of results
    bank_choices = GetInstitutions(bank_choice)
    num_banks = int(bank_choices['found'])

    # print(bank_choices['institutions'])
    # print(bank_choices['institutions'][0])
    # print(bank_choices['institutions'][0]['id'])
    # print(institution_dict)

    return render_template('showinstitutions.html', 
                            bank_choices = bank_choices, 
                            num_banks = num_banks)


@app.route('/institutionloginform', methods=['GET'])
@login_required
def institution_login():
    """Gets bank_id from the bank selected by the user, and generates the correct 
        login form. Add in detail in later version."""

    bank_id = request.args.get('select_bank')
    GetInstitutionLogin(bank_id)
    
    # BUILD OUT POST-HACKBRIGHT with Oauth

    # Save bank id number to session, shouldn't need after initial setup
    session['bank_id'] = bank_id

    return render_template('institutionlogin.html')


@app.route('/institutionlogin', methods=['POST'])
@login_required
def institution_form():
    """Allows users to login to their bank--REQUIRES OAUTH for actual banks. 
        Build out in later version."""

    # Gets data from institution login form (pretend login form for Finbank)
    banking_userid = request.form['banking_userid']
    banking_password = request.form['banking_password']
    # print(banking_userid)
    # print(banking_password)

    # Save banking_userid and banking_password to session, to add accounts
    session['banking_userid'] = banking_userid
    session['banking_password'] = banking_password

    return render_template('permission.html')


@app.route('/showaccounts')
@login_required
def add_accounts():
    """Displays results of account discovery for a particular customer/institution."""

    # Gets the user-selected value for permission to gather and display accounts
    permission = request.args.get('permission')

    if permission == 'no':
        flash('Are you sure? You cannot use essentially if you choose "Nope."')
        return render_template('permission.html')

    # Get these values from the Flask session
    customerId = session.get('fin_id')
    institutionId = session.get('bank_id')
    banking_userid = session.get('banking_userid')
    banking_password = session.get('banking_password')

    # print(customerId)
    # print(institutionId)
    # print(banking_userid)
    # print(banking_password)

    account_choices = DiscoverCustomerAccounts(customerId, institutionId, banking_userid, banking_password)
    
    session['account_choices'] = account_choices

    # print(account_choices)
   
    return render_template('showaccounts.html', account_choices = account_choices)


@app.route('/addaccounts')
@login_required
def show_accounts():
    """Allows users to select and add accounts from their chosen institution."""
    
    customerId = session.get('fin_id')
    # print(type(customerId))
    institutionId = session.get('bank_id')

    # Gets info on ALL (getlist) checkboxed accounts
    # account_choice = request.form['']
    account_choice = request.args.getlist('select_accounts')
    # print(account_choice)

    # Save account_choice in session for use in getting transactions
    session['account_choice'] = account_choice

    # Gets previous account info for all accounts that has been saved in session
    all_accounts_info = session.get('account_choices')
    # print(all_accounts_info)
    # print(all_accounts_info['accounts'])

    # Stores info in db and activates only selected accounts
    for account in all_accounts_info['accounts']:
        # print(account['id'])
        # print(type(account['id']))
        if str(account['id']) in account_choice:
            accountId = str(account['id'])
            accountNum = account['number'] 
            accountName = account['name']
            accountType = account['type']
            
            # Activate user accounts for daily transaction aggregation
            ActivateCustomerAccounts(customerId, institutionId, accountId, accountNum, accountName, accountType)
        
            # Add new user's account info to db
            new_user_accounts = UserBankAccount(fin_account_id = int(accountId),
                                                user_id = session.get('user_id'),
                                                account_name = accountName,
                                                account_num =  accountNum,
                                                account_type = accountType)
            
            db.session.add(new_user_accounts)
            
            # Gets all transactions for the last 12 months for each account (so there is data to pull from for categorizing)
            # PREMIUM FINICITY SERVICE ONLY (very sad)
            # GetHistoricCustomerTransactions(customerId, accountId)

    # Non-interactive refresh of customer transactions from all activated accounts
    RefreshCustomerAccounts(str(customerId))

    # fromDate = January 10, 2000, gets all transactions Finicity has for a given user
    fromDate = str(947462400)

    # Get all transactions for a certain customer within a given date range
    transactions = GetCustomerTransactions(customerId, fromDate)
    # print(transactions)

    # Loop through transactions to pick out the info that I want to store in the db
    for transaction in transactions['transactions']:
        if str(transaction['accountId']) in account_choice:
            fin_transaction_id = transaction['id']
            amount = transaction['amount']
            account = transaction['accountId']
            fin_description = transaction['memo']
            transaction_date = transaction['postedDate']

            # Add transactions to db, do inside for loop for each transaction
            new_user_transactions = Transaction(fin_transaction_id = fin_transaction_id,
                                            user_id = session.get('user_id'),
                                            amount = amount,
                                            account = account,
                                            fin_description =  fin_description,
                                            user_description = None,
                                            transaction_date = str(transaction_date),
                                            is_sorted = False)
            db.session.add(new_user_transactions)


    # Commits info for all accounts at once to db
    db.session.commit()

    get_transactions()

    return redirect('/showunsortedtransactions')


def get_transactions():
    """Collects new transactions for a specific customer."""

    user_id = session.get('user_id')
    # print(user_id)
    user_object = User.query.filter(User.user_id == user_id).first()
    # print(user_object)
    customerId = user_object.fin_id
    # print(customerId)

    # Non-interactive refresh of customer transactions from all activated accounts
    RefreshCustomerAccounts(str(customerId))
    
    # Set fromDate as the timestamp of the last recieved transaction stored in the db
    recentTransactObject = Transaction.query.filter(Transaction.user_id == user_id).order_by(Transaction.transaction_date.desc()).first()
    # print(recentTransactObject)
    fromDate = str(recentTransactObject.transaction_date)
    # print(fromDate)
    session['fromDate'] = fromDate

    # Get new transactions from Finicity
    new_transactions = GetCustomerTransactions(str(customerId), fromDate)

    user_account_choice = UserBankAccount.query.filter(UserBankAccount.user_id == user_id).all()
    # print(user_account_choice)

    account_choices = []

    for account in user_account_choice:
        added_account = account.fin_account_id
        account_choices.append(added_account)

    session['account_choices'] = account_choices

    # print(account_choices)

    # Loop through transactions to pick out the info that I want to store in the db
    for transaction in new_transactions['transactions']:
        if str(transaction['accountId']) in account_choices:
            fin_transaction_id = transaction['id']
            amount = transaction['amount']
            account = transaction['accountId']
            fin_description = random.choice(['target','chick-fil-a','starbucks','amazon','safeway','petco','chevron','home depot','blue bottle'])
            transaction_date = transaction['postedDate']

            # Add transactions to db, do inside for loop for each transaction
            newest_transactions = Transaction(fin_transaction_id = str(fin_transaction_id),
                                            user_id = session.get('user_id'),
                                            amount = amount,
                                            account = account,
                                            fin_description =  fin_description,
                                            user_description = None,
                                            transaction_date = str(transaction_date),
                                            is_sorted = False)

            db.session.add(newest_transactions)

    # Commits info for all accounts at once to db
    db.session.commit()


def query_for_unsorted_transactions(user_id):
    """Helper function to check if a specific user has unsorted transactions."""

    unsortedTransactObjects = Transaction.query.filter((Transaction.user_id == user_id) & (Transaction.is_sorted == False) & (Transaction.amount < 0)).all()
    # print(unsortedTransactObjects)

    return unsortedTransactObjects


def query_for_sorted_transactions(user_id):
    """Helper function to check if a specific user has unsorted transactions."""

    sortedTransactObjects = Transaction.query.filter((Transaction.user_id == user_id) & (Transaction.is_sorted == True) &  (Transaction.amount < 0)).all()
    # print(sortedTransactObjects)

    return sortedTransactObjects


@app.route('/showunsortedtransactions')
@login_required
def show_unsorted_transactions():
    """Displays unsorted transactions for a specific user if they have any."""

    # Get user_id from session
    user_id = session.get('user_id')

    # Check if unsortedTransactObjects contains objects
    unsorted_transactions = query_for_unsorted_transactions(user_id)
    
    if unsorted_transactions:
        for transaction in unsorted_transactions:
            # transaction.amount = '{0:.2f}'.format(transaction.amount)
            # print(amount) 
            # print(type(amount))
            transaction.transaction_date = time.strftime("%a, %b %-d", time.localtime(int(transaction.transaction_date)))
            transaction.fin_description = transaction.fin_description.title()
        return render_template('showunsortedtransactions.html', transactions = unsorted_transactions)
    # If unsortedTransactObjects is empty
    else: 
        # INSERT MESSAGE ABOUT YOU DON'T HAVE ANY TRANSACTIONS TO SORT???
        return redirect('/essentialvisual')


@app.route('/showsortedtransactions')
@login_required
def show_all_transactions():
    """Displays all sorted transactions for a specific user."""
   
    # Get user_id from session
    user_id = session.get('user_id')

    # Check if unsortedTransactObjects contains objects
    sorted_transactions = query_for_sorted_transactions(user_id)

    if sorted_transactions:
        for transaction in sorted_transactions:
            transaction.transaction_date = time.strftime("%a, %b %-d", time.localtime(int(transaction.transaction_date)))
            transaction.fin_description = transaction.fin_description.title()
        return render_template('showsortedtransactions.html', transactions = sorted_transactions)
    # If unsortedTransactObjects is empty
    else: 
        return redirect('/essentialvisual')


@app.route('/categorizetransactions', methods=['POST'])
@login_required
def categorize_transactions():
    """Allows users to categorize transactions as essential or non-essential."""

    # Get div id for the clicked transaction
    sorted_transaction = request.form.get('transaction_div_id')
    # print(sorted_transaction)
    # print(type(sorted_transaction_id))

    # Get the numerical transaction id for the clicked transaction
    sorted_transaction_id = sorted_transaction.split('-')[1]
    # print(sorted_transaction_id)

    # Get the category choice (T or F) for the clicked transaction
    sorted_transaction_category = request.form.get('category_choice')
    # print(sorted_transaction_category)

    # Change the string T or F to a boolean
    if sorted_transaction_category == 'T':
        sorted_transaction_category = True
    else:
        sorted_transaction_category = False


    # Add transaction categorization to db
    new_sorted_transaction = Transact_Category(transaction_id = sorted_transaction_id,
                                            category_choice = sorted_transaction_category)

    db.session.add(new_sorted_transaction)

    # Query for matching transaction_id in transactions table to update is_sorted boolean
    transaction_to_update = Transaction.query.filter(Transaction.transaction_id == sorted_transaction_id).first()
    # print(transaction_to_update)
    transaction_to_update.is_sorted = True

    # Commits info for all accounts at once to db
    db.session.commit()

    # print(sorted_transaction)
    return sorted_transaction


@app.route('/changecategory', methods=['POST'])
@login_required
def change_category():
    # Get div id for the clicked transaction
    changed_transaction = request.form.get('transaction_div_id')
    # print(changed_transaction)

    # Get the numerical transaction id for the clicked transaction
    changed_transaction_id = changed_transaction.split('-')[1]
    # print(changed_transaction_id)

    # Query for matching transaction_id in categorized_transactions table to update category_choice boolean
    transaction_to_update = Transact_Category.query.filter(Transact_Category.transaction_id == changed_transaction_id).first()
    # print(transaction_to_update)

    if transaction_to_update.category_choice == True:
        transaction_to_update.category_choice = False
    else:
        transaction_to_update.category_choice = True

    # Commits info for all accounts at once to db
    db.session.commit()
 
    return changed_transaction


@app.route('/essentialvisual')
@login_required
def display_essential_visual():
    """Displays the primary data visual."""

    # Get user_id from session
    user_id = session.get('user_id')

    # Check if sortedTransactObjects contains objects
    sorted_transactions = query_for_sorted_transactions(user_id)
    
    if not sorted_transactions:
        flash('Looks like you haven\'t sorted any transactions.')
    else: 
        num_non_essential = db.session.query(Transaction).join(Transact_Category)\
        .filter((Transact_Category.category_choice == False) & (Transaction.user_id == user_id)).all()
        # print(num_non_essential)
        num_essential = db.session.query(Transaction).join(Transact_Category)\
        .filter((Transact_Category.category_choice == True) & (Transaction.user_id == user_id)).all()
        # print(num_essential)

        non_essential_sum = 0
        for transaction in num_non_essential:
            non_essential_sum += transaction.amount

        essential_sum = 0
        for transaction in num_essential:
            essential_sum += transaction.amount

        category_sums = [-float("{0:.2f}".format(essential_sum)), -float("{0:.2f}".format(non_essential_sum))]
        # print(category_sums)

    return render_template('essentialvisual.html', category_sums = category_sums)


# @app.route('/institutioninfo')
# def display_institution_info():
#     """Displays detailed information about a selected institution."""

    # TODO LATER: Show detailed information on page where you add institutions? Don't need right now. 


@app.route('/logout')
def logout():
    """Allows the user to log out, ends the session."""

    if session.get('user_id'):
        for i in range(random.randint(1,10)):
            fin_transaction_id = ''.join(["%s" % random.randint(0, 9) for num in range(0, 10)]) 
            # print(fin_transaction_id)
            amount = -float(("{0:.2f}".format(random.random() * 10)))
            # print(amount)
            account = random.choice(session.get('account_choices'))
            # print(account)
            fin_description = random.choice(['target','chick-fil-a','starbucks','amazon','safeway','petco','chevron','home depot','blue bottle'])
            # print(fin_description)
            transaction_date = random.randint(int(session.get('fromDate')),int(round(time.time())))
            print(transaction_date)

                
            # Add transactions to db, do inside for loop for each transaction
            newest_transactions = Transaction(fin_transaction_id = str(fin_transaction_id),
                                            user_id = session.get('user_id'),
                                            amount = amount,
                                            account = account,
                                            fin_description =  fin_description,
                                            user_description = None,
                                            transaction_date = str(transaction_date),
                                            is_sorted = False)

            db.session.add(newest_transactions)

        # Commits info for all accounts at once to db
        db.session.commit()


        del session['user_id']
        # methods to delete the whole session
    return redirect('/loginform')

    # ************************* ADD LOGOUT BUTTON TO OTHER PAGES ******************** 



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


    # Use get Transaction details to display transactions to user
    # Let user select transactions, categorize, add categorizations to db
    # Use db to display info in donut chart
