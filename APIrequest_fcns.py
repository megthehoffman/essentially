import json
import requests 
import os

# ADD DOCSTRINGS AND DOCTESTS

def PartnerAuth():
    response = requests.post("https://api.finicity.com/aggregation/v2/partners/authentication", 
                            json={"partnerId": os.environ['PARTNER_ID'],
                            "partnerSecret": os.environ['PARTNER_SECRET']}, 
                            headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'], 
                            "Accept" : "application/json"})

    # print(response)
    # print(response.content)
    print(response.json())

    return response.json()["token"]


def GetInstitutions():
    # Need to call within each subsequent fcn, because it will expire every 2 hours
    token = PartnerAuth()
    # print(type(token))

    # Make searchInstitution a string that is returned from a form?
    # response = requests.get("https://api.finicity.com/aggregation/v1/institutions?search=" + searchInstitution,
    #                         headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
    #                         "Fincity-App-Token" : token,
    #                         "Accept" : "application/json"})

    response = requests.get("https://api.finicity.com/aggregation/v1/institutions?search=Wells+Fargo",
                            headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"})


    print(response.json())

    # return info to be stored in dd/get institutionId for GetInstutionLogin?


def GetInstitutionLogin():
    token = PartnerAuth()

    # Login is required for Discover Customer Accounts endpoint, provides form fields?

    #institutionId needs to be stored from GetInstitution?
    # response = requests.get("https://api.finicity.com/aggregation/v1//aggregation/v1/institutions/{institutionId}/loginForm",
    #                         headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
    #                         "Finicity-App-Token" : token,
    #                         "Accept" : "application/json"})

    response = requests.get("https://api.finicity.com/aggregation/v1/institutions/31/loginForm",
                            headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"})

    # print(response)
    print(response.json())

def AddTestingCustomer():
    token = PartnerAuth()

    response = requests.post("https://api.finicity.com/aggregation/v1/customers/testing",
                            json= "username" : username, 
                            "firstName" : fname, 
                            "lastName" : lname,
                            headers={"Finicity-App-Key" : os.environ['FINICITY_APP_KEY'],
                            "Finicity-App-Token" : token,
                            "Accept" : "application/json"})



