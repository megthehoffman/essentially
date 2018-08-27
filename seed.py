# Included because we want jinja to fail loudly, otherwise failure will be unknown
from jinja2 import StrictUndefined
import os
import re
import pdb
from APIrequest_fcns import *
import bcrypt
import time
import random
from flask import Flask, render_template, redirect, request, flash, session
from server import app
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Transaction, Transact_Category, Password, Security, UserBankAccount
# What does this do?
from warnings import warn

def run():
    # Get user from db
    user = get_user('eduardocat')
    user_id = user.user_id
    print(user_id)
    print(user.user_bank_accounts[0].fin_account_id)

    # Add testing transactions
    # AddTestingTransactions(str(user.fin_id), str(user.user_bank_accounts[0].fin_account_id), str(50.50), 'cat', '1534896000', '1534895000')
    # print(response.content)

    # Get customer transactions
    # fromDate = January 10, 2000
    fromDate = str(947462400)

    # Get all transactions for a certain customer within a given date range
    transactions = GetCustomerTransactions(str(user.fin_id), fromDate)
    print(transactions)

def get_user(username):

    user_in_db = User.query.filter(User.username == username).first()

    return user_in_db


if __name__ == "__main__":
    
    connect_to_db(app)

    run()