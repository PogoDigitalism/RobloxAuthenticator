from authenticator import TradeAuthenticator, TradeAuthenticatorAsync

t = TradeAuthenticator()
t.add(USER_ID = 98452948, 
      OTP_SECRET = 'OTPSECRETHERE', 
      RBLX_COOKIE = 'ROBLOSECURITYCOOKIEHERE', 
      TAG = 'acc1')

t.accept_trade('acc1', TRADE_ID = YOURIDHERE)
