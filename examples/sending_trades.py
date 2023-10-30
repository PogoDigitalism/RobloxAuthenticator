from utils import Formatting
from authenticator import TradeAuthenticator, TradeAuthenticatorAsync

t = TradeAuthenticator()
t.add(USER_ID = 98452948, 
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

data = utils.Formatting.TradeData(SENDER_USER_ID = 98452948, 
                                  RECIPIENT_USER_ID = 89389334, 
                                  OFFER = [19873344479], 
                                  REQUEST = [59884936856], 
                                  ROBUX = 35, 
                                  RECIPIENT_ROBUX = 230)

t.send_trade('acc1', data)
