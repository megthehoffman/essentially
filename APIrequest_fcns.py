import json
import requests 
import os
import time

# ADD DOCSTRINGS AND DOCTESTS
# ADD CORRECT RETURN STATEMENTS TO ALL FCNS

def PartnerAuth():
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


def GetInstitutions(searchInstitution):
    """Takes in a string input by the user in a form, searchInstitute, and queries API for institutions (banks)."""

    # Need to call within each subsequent fcn, because it will expire every 2 hours
    token = PartnerAuth()
    # print(type(token))
    # print(token)

    # Make searchInstitution a string that is returned from a form?
    response = requests.get("https://api.finicity.com/aggregation/v1/institutions?search=" + searchInstitution,
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
    print(response.json())
    return str(response.json()["institutions"][0]["id"])


    #Display all of the bank options, then have event listener--store bank id for one user clicks on
    
    # return response.json()


    # Call GetInstitutionLogin here?
    # return info to be stored in dd/get institutionId for GetInstutionLogin?


def GetInstitutionLogin(institutionId):
    """Takes in institutionId from GetInstitutions and gets login form for that institution. Login
    is required for Discover Customer Accounts API endpoint."""

    token = PartnerAuth()

    response = requests.get("https://api.finicity.com/aggregation/v1/institutions/" + institutionId + "/loginForm",
                            headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                            })

    # print(response)
    print(response.json())

    return response.json()


def AddTestingCustomer(username, fname, lname): 
    token = PartnerAuth()

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


def GetCustomer(customerId):
    """Takes in a customerId, gets details for the given customer."""

    token = PartnerAuth()

    response = requests.get("https://api.finicity.com/aggregation/v1/customers/" + customerId,
                            headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                            })

    print(response.json())
    # Printout looks like: {'id': '24957805', 'username': 'mhoffman', 'firstName': 'Megan', 'lastName': 'Hoffman', 
    #                       'type': 'testing', 'createdDate': '1533855225'}



def DiscoverCustomerAccounts(customerId, institutionId): 
    """Query for all accounts associated with a given customerId at a given institutionId."""

    token = PartnerAuth()

    response = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customerId + 
                            "/institutions/" + institutionId + "/accounts",
                            json= {
                               "credentials": [
                                  {
                                     "id": "101732001",
                                     "name": "Banking Userid",
                                     "value": "demo"
                                  },
                                  {
                                     "id": "101732002",
                                     "name": "Banking Password",
                                     "value": "go"
                                  }
                               ]
                            },
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })
    print(response.json())


# def ActivateCustomerAccounts(customerId, institutionId):
#     """Activates the specified customer accounts for daily transaction aggregation."""

#     token = PartnerAuth()

#     reponse = requests.post("https://api.finicity.com/aggregation/v2/customers/" + customerId +
#                             "/institutions/" + institutionId + "/accounts",
#                             json={
#                                "account": 
#                                {
#                                   "id": PASS,
#                                   "number": IN,
#                                   "name": THINGS,
#                                   "type": FROM ADD FCN
#                                }
#                             },
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     print(response.json())

    # ADD EVENT LISTENER--IF USER CLICKS ON ACCOUNT, ACTIVATE


def RefreshCustomerAccounts(customerId):
    """Queries for all transactions related to a given customerId, a non-interative refresh."""

    token = PartnerAuth()

    reponse = requests.post("https://api.finicity.com//aggregation/v1/customers/" + customerId + "/accounts",
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })

    print(response.json())


def GetHistoricCustomerTransactions(customerId, accountId):
    """Loads transactions from past 180 days for a specific customerId. Accessible via GetCustomerTransactions.
        Does not return anything."""

    token = PartnerAuth()

    response = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customerId + 
                            "/accounts/" + accountId + "/transactions/historic",
                            headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })


def GetCustomerTransactions(customerId, fromDate):
    """Queries for all transactions for a given customerId, between a specific date range."""

    token = PartnerAuth()
    toDate = str(int(time.time()))
    print(toDate)

    response = requests.get("https://api.finicity.com/aggregation/v3/customers/" + customerId + 
                            "/transactions?fromDate=" + fromDate + "&toDate=" + toDate,
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })

    print(response.json())


def GetCustomerTransactionDetails(customerId, transactionId):
    """Gets details for a specific transactionId."""

    token = PartnerAuth()

    response = requests.get("https://api.finicity.com/aggregation/v2/customers/" + customerId +
                            "/transactions/" + transactionId,
                            headers={
                            "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"
                            })

    print(response.json())


def DeleteCustomer(customerId):
    """Deletes an entire customer and associated accounts with no confirmation.
        USE CAREFULLY! Does not return anything."""

    token = PartnerAuth()

    response = requests.delete("https://api.finicity.com/aggregation/v1/customers/" + customerId,
                                headers={
                                "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                                "Finicity-App-Token" : token,
                                "Accept" : "application/json"
                                })

    print(customerId + " has been deleted! Hope you actually wanted to do that.")







