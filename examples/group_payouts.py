from utils import Formatting
from authenticator import Authenticator
from exceptions import *

t = Authenticator()
t.add(USER_ID = 98452948, # make sure this is the group holder, only the holder can make payout requests
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

data = Formatting.OneTimePayout(PAYOUT_RECIPIENT_USER_ID = 98452948, ROBUX = 10)

try:
    t.one_time_payout('acc1', GROUP_ID = 10435498, PAYOUT_DATA = data)
except AlreadyProcessedError:
    # Do whatever u want here if it processed without authentication
    pass
