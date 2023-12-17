from utils import Formatting
from authenticator import Authenticator
from exceptions import *

t = Authenticator()
t.add(USER_ID = 98452948, # make sure this is the group holder, only the holder can make payout requests
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

data = Formatting.AccessoryPurchase(PRICE=100, SELLER_ID=1)

try:
    t.accessory_purchase('acc1', ACCESSORY_ID=15491726543, PURCHASE_DATA=data)
except (AlreadyProcessedError, APIError) as e:
    # Do whatever u want here if it processed without authentication
    pass
