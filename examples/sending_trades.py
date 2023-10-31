from utils import Formatting
from authenticator import Authenticator
from exceptions import *

t = Authenticator()
t.add(USER_ID = 98452948, 
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

data = Formatting.TradeData(SENDER_USER_ID = 98452948, 
                                  TRADE_RECIPIENT_USER_ID = 89389334, 
                                  OFFER = [19873344479], 
                                  REQUEST = [59884936856], 
                                  ROBUX = 35, 
                                  RECIPIENT_ROBUX = 230) #Formatting.TradeData is not required as it returns just a dictionairy that you could build yourselves. For the convenience however, a utility was added either way to easily format them.

try:
      t.send_trade(TAG = 'acc1', TRADE_DATA = data)
except AlreadyProcessedError:
    # Do whatever u want here if it processed without authentication
    pass
