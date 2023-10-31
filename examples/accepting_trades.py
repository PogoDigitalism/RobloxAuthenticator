from utils import Formatting
from authenticator import Authenticator
from exceptions import *

t = Authenticator()
t.add(USER_ID = 98452948, 
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

try:
    t.accept_trade('acc1', TRADE_ID = YOURIDHERE)
except AlreadyProcessedError:
    # Do whatever u want here if it processed without authentication
    pass
