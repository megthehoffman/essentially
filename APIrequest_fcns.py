import json
import requests 
import os
import time

# ADD DOCSTRINGS AND DOCTESTS
# ADD CORRECT RETURN STATEMENTS TO ALL FCNS

def partner_auth():
    """Queries API for a Finicity-App-Token, token expires every two hours."""

    response = requests.post("https://api.finicity.com/aggregation/v2/partners/authentication", 
                            json={
                                "partnerId": os.environ['PARTNER_ID'],
                                "partnerSecret": os.environ['PARTNER_SECRET']
                            }, 
                            headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'], 
                                "Accept" : "application/json"
                                })

    # print(response)
    # print(response.content)
    # print(response.json())
    # print(response.json()["token"])

    return response.json()["token"]


def get_institutions(search_institution):
    """Takes in a string input by the user in a form, searchInstitute, and queries API for institutions (banks)."""

    # Need to call within each subsequent fcn, because it will expire every 2 hours
    token = partner_auth()
    # print(type(token))
    # print(token)

    # Make search_institution a string that is returned from a form?
    response = requests.get("https://api.finicity.com/aggregation/v1/institutions?search=" + search_institution,
                            headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                            })


    # print(response)
    # print(response.headers)
    # print(response.request.url)   

    # for institution in response.json()["institutions"]:
    #     print(institution["id"])
        # Probably don't need to permanently store this, just want to use it

    # Gets all the information for the first bank in the list
    # print(response.json()["institutions"][0])

    # Just returning the id for the first bank
    # print(response.json())
    # return str(response.json()["institutions"][0]["id"])
    return response.json()


def get_institution_login(institution_id):
    """Takes in institution_id from get_institutions and gets login form for that institution. Login
    is required for Discover Customer Accounts API endpoint."""

    token = partner_auth()

    response = requests.get("https://api.finicity.com/aggregation/v1/institutions/" + institution_id + "/loginForm",
                            headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                            })

    # print(response)
    # print(response.json())

    return response.json()


def add_testing_customer(username, fname, lname): 
    token = partner_auth()

    # For fcns that require input from forms, call this fcn on the server side, and request.args.get/post info that is needed
    response = requests.post("https://api.finicity.com/aggregation/v1/customers/testing",
                            json={
                                "username" : username, 
                                "firstName" : fname, 
                                "lastName" : lname
                            },
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })
    # Printout looks like: {"id": "2495780", "username": "mhoffman", "createdDate": "1533855225"}
    # print(response.json())
    # print(type(response.json()))

    return response.json()


def get_customer(customer_id):
    """Takes in a customer_id, gets details for the given customer."""

    token = partner_auth()

    response = requests.get("https://api.finicity.com/aggregation/v1/customers/" + customer_id,
                            headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                            })

    return response.json()
    # Printout looks like: {'id': '24957805', 'username': 'mhoffman', 'firstName': 'Megan', 'lastName': 'Hoffman', 
    #                       'type': 'testing', 'createdDate': '1533855225'}



def discover_customer_accounts(customer_id, institution_id, banking_userid, banking_password): 
    """Query for all accounts associated with a given customer_id at a given institution_id."""

    token = partner_auth()

    response = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customer_id + 
                            "/institutions/" + institution_id + "/accounts",
                            json= {
                               "credentials": [
                                  {
                                     "id": institution_id +"001",
                                     "name": "Banking Userid",
                                     "value": banking_userid
                                  },
                                  {
                                     "id": institution_id + "002",
                                     "name": "Banking Password",
                                     "value": banking_password
                                  }
                               ]
                            },
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })
    # print(response.json())
    return response.json()


def activate_customer_accounts(customer_id, institution_id, account_id, account_num, account_name, account_type):
    """Activates the specified customer accounts for daily transaction aggregation."""

    token = partner_auth()

    response = requests.put("https://api.finicity.com/aggregation/v2/customers/" + customer_id +
                            "/institutions/" + institution_id + "/accounts",
                            json={
                               "accounts": [
                               {
                                  "id": account_id,
                                  "number": account_num,
                                  "name": account_name,
                                  "type": account_type
                               }]
                            },
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })
    # print(response.decode('utf-8'))
    # print(response.content)
    # print(response.json())
    return response.json()


def refresh_customer_accounts(customer_id):
    """Queries for all transactions related to a given customer_id, a non-interative refresh."""

    token = partner_auth()

    response = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customer_id + "/accounts",
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })

    # print(response.json())
    return None

# Don't seem to need this at the moment?
# def add_testing_transactions(customer_id, account_id, amount, description, posted_date, transaction_date):

#     token = partner_auth()

#     response = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customer_id + "/accounts/" + account_id + "/transactions",
#                             json={
#                                "amount": amount,
#                                "description": description,
#                                "postedDate": posted_date,
#                                "transactionDate": transaction_date
#                             },
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     # print(response)
#     return response


# def get_historic_customer_transactions(customer_id, account_id):
#     """Loads transactions from past 180 days for a specific customer_id. Accessible via get_customer_transactions.
#         Does not return anything."""

#     token = partner_auth()

#     response = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customer_id + 
#                             "/accounts/" + account_id + "/transactions/historic",
#                             headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     return response


def get_customer_transactions(customer_id, from_date):
    """Queries for all transactions for a given customer_id, between a specific date range."""

    token = partner_auth()
    to_date = str(int(round(time.time())))
    # print(type(to_date))

    response = requests.get("https://api.finicity.com/aggregation/v3/customers/" + customer_id + 
                            "/transactions?fromDate=" + from_date + "&toDate=" + to_date,
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })

    return response.json()


def get_customer_transaction_details(customer_id, transaction_id):
    """Gets details for a specific transaction_id."""

    token = partner_auth()

    response = requests.get("https://api.finicity.com/aggregation/v2/customers/" + customer_id +
                            "/transactions/" + transaction_id,
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })

    return response.json()


def delete_customer(customer_id):
    """Deletes an entire customer and associated accounts with no confirmation.
        USE CAREFULLY! Does not return anything."""

    token = partner_auth()

    response = requests.delete("https://api.finicity.com/aggregation/v1/customers/" + customer_id,
                                headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                                })

    print(customer_id + " has been deleted! Hope you actually wanted to do that.")

    return response.json()






