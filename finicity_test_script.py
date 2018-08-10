from APIrequest_fcns import *


# clean up errors from file in order to use

# Get partner token, returns just token as a string
PartnerAuth()


# Get institutions containing keyword
# Works without formatting, which is weird 
# GetInstitutions("Wells Fargo")
GetInstitutions("finbank")

# GetInstitutions("Bank of America")
# GetInstitutions("wellsfargo")
# GetInstitutions("well")


# Get login form info for a specific institution
# In this case, picks the first one in a list from a search of "Wells Fargo"
# GetInstitutionLogin(GetInstitutions("Wells Fargo"))
GetInstitutionLogin("101732")

# Adds testing customer
# AddTestingCustomer("mhoffman", "Megan", "Hoffman")


# Gets info about a specific customer
GetCustomer("24957805")

# Gets all accounts associated with a given customer
DiscoverCustomerAccounts("24957805", "101732")