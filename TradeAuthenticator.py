import base64
import json
import pyotp
import requests

class APIError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class _Account:
    def __init__(self, otp, ck, i_d) -> None:
        self.OTP_SECRET = otp
        self.RBLX_COOKIE = ck
        self.USER_ID = i_d


class TradeAuthenticator:
    """
    The synchronous wrapper for TradeAuthenticator.

    Please read the GitHub for all info that you need.
    https://github.com/PogoDigitalism/RobloxTradeAuthenticator/
    
    """
    VALIDATE_TYPES = {'USER_ID': str,
                  'OTP_SECRET': str,
                  'RBLX_COOKIE': str,
                  'TAG': str}   
    
    def __init__(self) -> None:
        self.__accs: dict[str, dict[str,int]] = dict()
        self.__current_account = str()
        self.__current_session = requests.Session()

    @staticmethod
    def __validate(_locals: dict) -> bool | None:
        """Private method. """
        for _k in _locals:
            if not isinstance(_locals[_k], TradeAuthenticator.VALIDATE_TYPES[_k]):
                raise NotImplementedError(f'Invalid type "{type(_locals[_k])}" for {_k}.\n\n--> Use the proper types that are hinted.')
        return True
    
    @staticmethod
    def __secrTo6Digi(OTP_SECRET: str) -> str:
        """Private method. """
        return pyotp.TOTP(OTP_SECRET).now()
    
    def __getXCSRF(self) -> str:
        """Private method. """
        get_token = self.__current_session.post("https://auth.roblox.com/v2/logout",cookies={".ROBLOSECURITY": self.__accs[self.__current_account]['RBLX_COOKIE']})
        if get_token.status_code == 200:
            return get_token.headers["x-csrf-token"]
        else:
            j = get_token.json()
            raise APIError(f'APIError for __getXCSRF:\n\n{get_token.status_code}, {j}')
        
    def __getChallengeID(self, XCSRF, TRADE_ID) -> str:
        """Private method. """
        r_init = self.__current_session.post(url=f"https://trades.roblox.com/v1/trades/{TRADE_ID}/accept",headers={'x-csrf-token': XCSRF ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": self.__accs[self.__current_account]['RBLX_COOKIE']})
        if r_init.status_code == 200:
            return False
        elif r_init.status_code == 400:
            return json.loads(base64.b64decode(r_init.headers.get('rblx-challenge-metadata')).decode("UTF-8"))['challengeId'], r_init.headers.get('rblx-challenge-id'), r_init.headers.get('rblx-challenge-type')
        else:
            j = r_init.json()
            raise APIError(f'APIError for __getChallengeID:\n\n{r_init.status_code}, {j}')
        
    def __twoStep(self, XCSRF, CHALLENGE_MD) -> str:
        """Private method. """
        r_verify = self.__current_session.post(url=f"https://twostepverification.roblox.com/v1/users/{self.__accs[self.__current_account['USER_ID']]}/challenges/authenticator/verify"
                ,headers={'x-csrf-token': XCSRF ,"Content-Type": "application/json"}
                ,cookies={".ROBLOSECURITY": self.__accs[self.__current_account['RBLX_COOKIE']]}
                ,data=json.dumps({
                    'actionType': "Generic",
                    'challengeId': CHALLENGE_MD,
                    'code': TradeAuthenticator.__secrTo6Digi(self.__accs[self.__current_account['OTP_SECRET']])
                }))
        
        if r_verify.status_code == 200:
            Verification_MetaData = {
                'verificationToken': r_verify.json()['verificationToken'],
                'rememberDevice': True,
                'challengeId': CHALLENGE_MD,
                'actionType': "Generic"
            }
            return base64.b64encode(json.dumps(Verification_MetaData).encode("UTF-8"))
        else:
            j = r_verify.json()
            raise APIError(f'APIError for __twoStep:\n\n{r_verify.status_code}, {j}')
        
    def add(self, USER_ID: str , OTP_SECRET: str, RBLX_COOKIE: str, TAG: str = None) -> dict:
        """
        Adds a new  account to the account cache.
        Can be called in other commands and can not be configured.
        
        :param str USER_ID: Roblox user ID to attach to the cachced account.
        :param str OTP_SECRET: OTP Secret string (Check the GitHub for more info).
        :param str RBLX_COOKIE: Your _ROBLOSECURITY cookie.
        :param str TAG: [OPTIONAL] Add a tag to the added account to index it easily later and use its data.
        
        """
        _l = locals()
        _l.pop('self')
        TradeAuthenticator.__validate(_l)
        
        if not TAG:
            TAG = USER_ID
        
        _D: dict = _Account(OTP_SECRET, RBLX_COOKIE, USER_ID).__dict__
        self.__accs[TAG] = _D
        return _D
    
    def config(self, TAG: str, UPDATED_INFO: dict[str, str]) -> dict:
        """
        Configure a cached account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        :param dict UPDATED_INFO: Invalid key value pairs will raise a *KeyError* or *NotImplementedError*.
        
        """
        if not isinstance(TAG, str):
            raise NotImplementedError('TAG should be a string.')
        
        TradeAuthenticator.__validate(UPDATED_INFO)
        
        for _k in UPDATED_INFO:
            self.__accs[TAG][_k] = UPDATED_INFO[_k]
            
        return self.__accs[TAG]
    
    def remove(self, TAG: str) -> bool:
        """
        Remove an account from the cache.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        
        """
        if self.__accs.get(TAG):
            self.__accs.pop(TAG)
            return True
        raise KeyError(f'{TAG} does not exist in account cache.')    
    
    def accept_trade(self, TAG: str, TRADE_ID: int) -> dict:
        """
        Accept a trade with the speficied account (through TAG) and the TRADE_ID of the trade that you want to accept.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param str TRADE_ID: Speaks for itself. Make sure its the valid one though :)     
        
        """
        if not self.__accs.get(TAG):
            raise KeyError(f'{TAG} does not exist in account cache.')
        
        self.__current_account = TAG
        self.__current_session = requests.session()
        
        XCSRF = self.__getXCSRF()
        
        CHALLENGE_MD, CHALLENGE_ID, CHALLENGE_TYPE = self.__getChallengeID(XCSRF, TRADE_ID)
        
        FINAL_CMD = self.__twoStep(XCSRF, CHALLENGE_MD)
        
        r_accept = self.__current_session.post(url=f"https://trades.roblox.com/v1/trades/{TRADE_ID}/accept",headers={'rblx-challenge-id': CHALLENGE_ID,'rblx-challenge-metadata': FINAL_CMD,'rblx-challenge-type': CHALLENGE_TYPE,'x-csrf-token': XCSRF ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": self.__accs[self.__current_account['RBLX_COOKIE']]})
        j = r_accept.json()
        if r_accept.status_code == 200:
            return j
        else:
            raise APIError(f'APIError for accept_trade:\n\n{r_accept.status_code}, {j}')
    
    def info(self, TAG: str) -> dict:
        """
        Get the data of an account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        
        """
        if self.__accs.get(TAG):
            return self.__accs[TAG]
        raise KeyError(f'{TAG} does not exist in account cache.')
    
    def __repr__(self) -> str:
        return f'{self.__accs}'
