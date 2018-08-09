from APIrequest_fcns import *


# clean up errors from file in order to use

# Get partner token, returns just token as a string
PartnerAuth()

# Get institutions containing keyworkd 
GetInstitutions("Wells Fargo")
GetInstitutions("Bank of America")