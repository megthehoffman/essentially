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

class User(db.Model):
    """Users model. User refers to app User, whereas Customer refers to Finicity user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fin_id = db.Column(db.Integer, nullable=False) 
        # fin_id is id created when Customer is created
    created_date = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__ (self):
        """Provide helpful information when printed."""

        return f"""<User user_id={self.user_id} 
                fin_id={self.fin_id} 
                created_date={self.created_date}
                fname={self.fname}
                username={self.username}
                >"""


class Transaction(db.Model):
    """Transactions model. Will store information about all transactions for all users."""

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fin_transaction_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.Float(7,2), nullable=False)
    fin_description = db.Column(db.String(100), nullable=False)
        # Description provided by Finicity
    user_description = db.Column(db.String(25), nullable=True)
        # Add ability for user to change this later
    transaction_date = db.Column(db.DateTime(), nullable=False)


    # Put relationships where the foriegn key is located
    # Relationships return a new property that can do multiple things
    # This relationship lets me look at a transaction and get the user_id
    # Backref allows me to look at user and get all transactions, using new property
    # EX: user_id.transactions for easier querying
    user = db.relationship("User", backref=db.backref("transactions"))

    def __repr__ (self):
        """Provide helpful information when printed."""

        return f"""<Transaction transaction_id={self.transaction_id}
                user_id={self.user_id} 
                amount={self.amount}
                >"""


class Transact_Category(db.Model):
    """Category model. Will store how transactions have been categorized by users."""

    __tablename__ = "categorized_transactions"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), 
                    nullable=False)
    category_choice = db.Column(db.Boolean(), nullable=False)
    # T = essential, F = non-essential

    # This relationships associates a category_choice with a transaction_id
    # Backref allows querying of category_choice using transaction_id
    transaction = db.relationship("Transaction", backref=db.backref("category"))

    def __repr__ (self):
        """Provide helpful information when printed."""

        return f"""<Category category_id={self.category_id}
                transaction_id={self.transaction_id}
                category={self.category}
                >"""


class UserBankAccount(db.Model):
    """UserBankAccount model. Will store information about all selected accounts for all users."""

    __tablename__ = "user_bank_accounts"

    account_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fin_account_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_num =  db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(100), nullable=False)

    # Put relationships where the foriegn key is located
    # Relationships return a new property that can do multiple things
    # This relationship associates an account_id a user_id
    user = db.relationship("User", backref=db.backref("user_bank_accounts"))

    def __repr__ (self):
        """Provide helpful information when printed."""

        return f"""<UserBankAccount fin_account_id={self.fin_account_id}
                user_id={self.user_id} 
                account_name={self.account_name}
                >"""


class Password(db.Model):
    """Password model. Will store hashed user passwords, and possibly security question
    answers."""

    __tablename__ = "passwords"

    password_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    hash_pass = db.Column(db.String(500), nullable=False)
    # CAN USE THIS COLUMN LATER TO ALLOW FOR MULTIPLE PASSWORDS OR MULTIPLE VERSIONS OF PASSWORDS
    current_pass = db.Column(db.Boolean(), nullable=True)
    securityq_id = db.Column(db.Integer, db.ForeignKey('security_questions.securityq_id'),
                    nullable=True)
    securityq_ans = db.Column(db.String(100), nullable=True)
    # NEED TO HASH SECURITY ANSWER IF DONE LATER

    # Create a relationship between Password and Security via the securityq_id fkey
    security = db.relationship("Security")

    # Backref allows access to password via user_id
    user = db.relationship("User", backref=db.backref("passwords"))

    def __repr__ (self):
        """Provide helpful information when printed."""

        return f"""<Password password_id={self.password_id}
                    user_id={self.user_id} 
                    hash_pass={self.hash_pass}
                    >"""


class Security(db.Model):
    """Security model. Will store security questions that users will choose from to answer."""

    __tablename__ = "security_questions"

    securityq_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    securityq = db.Column(db.Text(), nullable=False)

    def __repr__ (self):
        """Provide helpful information when printed."""

        return f"""<Security securityq_id={self.securityq_id}
                    securityq={self.securityq} 
                    >"""


# HELPER FCNS

def init_app():
    # So that we can use Flask-SQLAlchemy
    app = Flask(__name__)
    connect_to_db(app)
    # Need this to create actual tables with columns, even if empty
    db.create_all()

    print("You're connected!")

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    # This is the database URI that should be used for the connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///essentially'
    # If set to true, SQLAlchemy will log errors, useful for debugging
    app.config['SQLALCHEMY_ECHO'] = False
    # If set to true, SQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If this module is run interactively, can work with the db directly

    init_app()
