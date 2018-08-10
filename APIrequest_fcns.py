import json
import requests 
import os

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

    # hardcoded Wells Fargo as a sample, need to format search input with + sign
    # response = requests.get("https://api.finicity.com/aggregation/v1/institutions?search=Wells+Fargo",
    #                         headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
    #                         "Finicity-App-Token" : token,
    #                         "Accept" : "application/json"})


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
    # Printout looks like: {"id": "24957805", "username": "mhoffman", "createdDate": "1533855225"}
    # print(response.json())
    # print(type(response.json()))

    # CAN ONLY DO THIS ONCE PER USER/USERNAME
    # DO IT AND STORE ALL NEEDED INFO IN DB

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
        # TEST institutionsId is 101732

    token = PartnerAuth()


#     reponse = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customerId + 
#                             "/institutions/" + institutionId + "/accounts",
#                             json= { # will need to use a list or something like that
#                                 "accounts" : {
#                                     "credentials": [
#                                         {
#                                             "id": # FROM INSTITUTION LOGIN FORM
#                                             "name":
#                                             "value":
#                                         },
#                                         {
#                                             "id":
#                                             "name":
#                                             "value":
#                                         }
#                                     ]
#                                 }
#                             },
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })
#     print(response.json())


# def AddAllAccounts(customerId, institutionId):
#     """Adds all accounts associated with a given customerId at a given institutionId."""

#     token = PartnerAuth()

#     # SAME JSON AS DiscoverCustomerAccounts, get info with list

#     # will need to turn arguments into strings
#     reponse = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customerId + 
#                             "/institutions/" + institutionId + "/accounts/addall",
#                             json=,
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     print(response.json())


# def RefreshCustomerAccounts(customerId):
#     """Queries for all transactions related to a given customerId, a non-interative refresh."""

#     token = PartnerAuth()

#     reponse = requests.post("https://api.finicity.com/aggregation/v1/customers/" + customerId + "/accounts",
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     print(response.json())


# def GetCustomerTransactions(customerId, fromDate, toDate):
#     """Queries for all transactions for a given customerId, between a specific date range."""

#     token = PartnerAuth()

#     response = requests.get("https://api.finicity.com/aggregation/v3/customers/" + customerId + 
#                             "/transactions?fromDate=" + fromDate + "&toDate=" + toDate,
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     print(response.json())


# def GetCustomerTransactionDetails(customerId, transactionId):
#     """Gets details for a specific transactionId."""

#     token = PartnerAuth()

#     response = requests.get("https://api.finicity.com/aggregation/v2/customers/" + customerId +
#                             "/transactions/" + transactionId,
#                             headers={
#                             "Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
#                             "Finicity-App-Token" : token,
#                             "Accept" : "application/json"
#                             })

#     print(response.json())








