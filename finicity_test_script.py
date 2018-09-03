from APIrequest_fcns import *


# clean up errors from file in order to use

# Get partner token, returns just token as a string
partner_auth()


# Get institutions containing keyword
# Works without formatting, which is weird 
# get_institutions("Wells Fargo")
get_institutions("finbank")

# get_institutions("Bank of America")
# get_institutions("wellsfargo")
# get_institutions("well")


# Get login form info for a specific institution
# In this case, picks the first one in a list from a search of "Wells Fargo"
# get_institution_login(get_institutions("Wells Fargo"))
get_institution_login("101732")

# Adds testing customer
# add_testing_customer("mhoffman", "Megan", "Hoffman")


# Gets info about a specific customer
get_customer("24957805")

# Gets all accounts associated with a given customer
discover_customer_accounts("24957805", "101732")