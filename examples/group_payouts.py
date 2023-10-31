from utils import Formatting
from authenticator import Authenticator
from exceptions import *

t = Authenticator()
t.add(USER_ID = 98452948, 
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

data = Formatting.OneTimePayout(RECIPIENT_USER_ID = 98452948, ROBUX = 10)

try:
    t.one_time_payout('acc1', 10435498, data)
except AlreadyProcessedError:
    # Do whatever u want here if it processed without authentication
    pass
