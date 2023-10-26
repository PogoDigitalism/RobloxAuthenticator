import base64
import json
import ast
import pyotp
import requests
import aiohttp
import math
import config
import utils
import warnings

from typing import Any, Union, Optional

class APIError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AlreadyProcessedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class _Account:
    def __init__(self, otp, ck, i_d) -> None:
        self.OTP_SECRET = otp
        self.RBLX_COOKIE = ck
        self.USER_ID = i_d

class Validate:
    VALIDATE_TYPES = {'USER_ID': str,
                  'OTP_SECRET': str,
                  'RBLX_COOKIE': str,
                  'TAG': str,
                  
                  'OFFER': list,
                  'REQUEST': list,
                  
                  'TRADE_RECIPIENT_USER_ID': int,
                  'SENDER_USER_ID': int,
                  'RECIPIENT_ROBUX': int,
                  'ROBUX': int}   

    @staticmethod
    def _types(_locals: dict[str, any]) -> bool | None:
        """Private method. """
        for _k in _locals:
            try: _locals[_k]
            except KeyError: raise KeyError(f'{_k} is not a valid keyword argument.')
            if not isinstance(_locals[_k], Validate.VALIDATE_TYPES[_k]):
                raise NotImplementedError(f'Invalid type "{type(_locals[_k])}" for {_k}.\n\n--> Use the proper types that are hinted.')
        return True

class Formatting:
    def __validate(func):
        def wrapper(*args, **kwargs):
            Validate._types(kwargs)

            result = func(*args, **kwargs)
            return result
        return wrapper

    @staticmethod
    @__validate
    def TradeData(SENDER_USER_ID: int, TRADE_RECIPIENT_USER_ID: int, REQUEST: list, OFFER: list, ROBUX: int = 0, RECIPIENT_ROBUX: int = 0) -> dict[str, dict[str, Union[list, int]]]:
        """Formats your data into a dictionairy that can be used for sending and countering trades."""
        return {
        "offers": [
            {
            "userId": SENDER_USER_ID,
            "userAssetIds": OFFER,
            "robux": abs(ROBUX)
            },
            {
            "userId": TRADE_RECIPIENT_USER_ID,
            "userAssetIds": REQUEST,
            "robux": abs(RECIPIENT_ROBUX)
        }
            ]
        }

class TradeAuthenticator:
    """
    The synchronous wrapper for TradeAuthenticator.

    Please read the GitHub for all info that you need.
    https://github.com/PogoDigitalism/RobloxTradeAuthenticator/
    
    """  
    def __init__(self) -> None:
        self.__accs: dict[str, dict[str,int]] = dict()
        self.__current_account = str()
        self.__current_session = requests.Session()

    def __validate(func):
        def wrapper(*args, **kwargs):
            Validate._types(kwargs)

            result = func(*args, **kwargs)
            return result
        return wrapper
    
    def __ExecuteSequence(self, **kwargs):
        METHOD = kwargs['METHOD']
        INIT_DATA: dict = kwargs['INIT_DATA']
        
        VAR_DICT = {'Content-Type': 'application/json', 'actionType': 'Generic'}
        VAR_DICT['.ROBLOSECURITY'] = self.__accs[self.__current_account['RBLX_COOKIE']]
        
        sequence = config.Config._Sequence(METHOD)
        httpConfig = config.Config.httpConfig
        urlConfig = config.Config.urlConfig
        
        resp: requests.Response
        for httpMethod in sequence:
            methodInfo = httpConfig[httpMethod]
            
            methodHeaders = methodInfo['HEADERS']
            headersSubmit = {}
            for h in methodHeaders:
                headersSubmit[h] = VAR_DICT[h]
                
            methodData = methodInfo['DATA']
            if not isinstance(methodData, str):
                dataSubmit = {}
                for d in methodData:
                    if d == 'code':
                        dataSubmit[d] = utils.privUtils.__secrTo6Digi(self.__accs[self.__current_account['OTP_SECRET']])
                    else:
                        dataSubmit[d] = VAR_DICT[h]
            else: #custom data util prepare for 'send'
                dataSubmit = kwargs['INIT_DATA']['POSTDATA']
                
            methodCookies = methodInfo['COOKIES']
            cookiesSubmit = {}
            for c in methodCookies:
                cookiesSubmit[c] = VAR_DICT[c]


            if methodInfo['URL'] is None:
                url = urlConfig[httpMethod][METHOD]
            else:
                url = methodInfo['URL']
            
            if '$' in url:
                a_url = url.split('$')[0]
                b_url = url.split('$')[1]

                var = b_url.split('$')[0]
                b_url = b_url.split('$')[1]
                
                url = f'{a_url}{str(INIT_DATA.get(var))}{b_url}'

            if methodInfo['METHOD'] == 'POST':
                resp = self.__current_session.post(url, data=dataSubmit, headers=headersSubmit, cookies=cookiesSubmit)
            elif methodInfo['METHOD'] == 'GET':
                resp = self.__current_session.get(url, data=dataSubmit, headers=headersSubmit, cookies=cookiesSubmit)
                
            if resp.status_code in methodInfo['STATUS']:
                for respHeader in methodInfo['RETURN_HEADERS']:    
                    VAR_DICT[respHeader] = resp.headers.get(respHeader)
                    
                if methodInfo['PROCESSING']:
                    VAR_DICT[methodInfo['PROCESSING'][1]] = getattr(utils.privUtils, methodInfo['PROCESSING'][0])(resp, VAR_DICT)
            else:
                if resp.status_code == 200:
                    raise AlreadyProcessedError('No authentication needed.')
                else:
                    raise APIError(f'HTTP Request failed\n\n{resp.status_code}: {resp.json()}')
                
        self.__current_session.close()
        return resp   
        
    # def __getXCSRF(self) -> str:
    #     """Private method. """
    #     get_token = self.__current_session.post("https://auth.roblox.com/v2/logout",cookies={".ROBLOSECURITY": self.__accs[self.__current_account]['RBLX_COOKIE']})
    #     if get_token.status_code == 200:
    #         return get_token.headers["x-csrf-token"]
    #     else:
    #         j = get_token.json()
    #         raise APIError(f'APIError for __getXCSRF:\n\n{get_token.status_code}, {j}')
        
    # def __getChallengeID(self, XCSRF, TRADE_ID, METHOD) -> str:
    #     """Private method. """
    #     _format = ''
    #     if METHOD == 1: _format += f'{TRADE_ID}/accept' 
    #     elif METHOD == 2: _format += 'send'
        
    #     r_init = self.__current_session.post(url=f"https://trades.roblox.com/v1/trades/{TRADE_ID}/accept",headers={'x-csrf-token': XCSRF ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": self.__accs[self.__current_account]['RBLX_COOKIE']})
    #     if r_init.status_code == 200:
    #         return False,False,False
    #     elif r_init.status_code == 400 or r_init.status_code == 401:
    #         return json.loads(base64.b64decode(r_init.headers.get('rblx-challenge-metadata')).decode("UTF-8"))['challengeId'], r_init.headers.get('rblx-challenge-id'), r_init.headers.get('rblx-challenge-type')
    #     else:
    #         j = r_init.json()
    #         raise APIError(f'APIError for __getChallengeID:\n\n{r_init.status_code}, {j}')
        
    # def __twoStep(self, XCSRF, CHALLENGE_MD) -> str:
    #     """Private method. """
    #     r_verify = self.__current_session.post(url=f"https://twostepverification.roblox.com/v1/users/{self.__accs[self.__current_account['USER_ID']]}/challenges/authenticator/verify"
    #             ,headers={'x-csrf-token': XCSRF ,"Content-Type": "application/json"}
    #             ,cookies={".ROBLOSECURITY": self.__accs[self.__current_account['RBLX_COOKIE']]}
    #             ,data=json.dumps({
    #                 'actionType': "Generic",
    #                 'challengeId': CHALLENGE_MD,
    #                 'code': TradeAuthenticator.__secrTo6Digi(self.__accs[self.__current_account['OTP_SECRET']])
    #             }))
        
    #     if r_verify.status_code == 200:
    #         Verification_MetaData = {
    #             'verificationToken': r_verify.json()['verificationToken'],
    #             'rememberDevice': True,
    #             'challengeId': CHALLENGE_MD,
    #             'actionType': "Generic"
    #         }
    #         return base64.b64encode(json.dumps(Verification_MetaData).encode("UTF-8"))
    #     else:
    #         j = r_verify.json()
    #         raise APIError(f'APIError for __twoStep:\n\n{r_verify.status_code}, {j}')
        
    @__validate
    def add(self, USER_ID: str , OTP_SECRET: str, RBLX_COOKIE: str, TAG: str = None) -> dict:
        """
        Adds a new  account to the account cache.
        Can be called in other commands.
        
        :param str USER_ID: Roblox user ID to attach to the cached account.
        :param str OTP_SECRET: OTP Secret string (Check the GitHub for more info).
        :param str RBLX_COOKIE: Your _ROBLOSECURITY cookie.
        :param str TAG: [OPTIONAL] Add a tag to the added account to index it easily later and use its data. If TAG is left empty, its value will be the USER_ID .
        
        """
        _l = locals()
        _l.pop('self')
        # Validate._types(_l)
        
        if not TAG:
            TAG = USER_ID
        
        _D: dict = _Account(OTP_SECRET, RBLX_COOKIE, USER_ID).__dict__
        self.__accs[TAG] = _D
        return _D
    
    @__validate
    def config(self, TAG: str, UPDATED_INFO: dict[str, str]) -> dict:
        """
        Configure a cached account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        :param dict UPDATED_INFO: Invalid key value pairs will raise a *KeyError* or *NotImplementedError*.
        
        """
        if not isinstance(TAG, str):
            raise NotImplementedError('TAG should be a string.')
        
        # Validate._types(UPDATED_INFO)
        
        for _k in UPDATED_INFO:
            self.__accs[TAG][_k] = UPDATED_INFO[_k]
            
        return self.__accs[TAG]
    
    @__validate
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
    
    @__validate
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
        
        self.__ExecuteSequence(METHOD='ACCEPT', INIT_DATA={'USER_ID': self.__accs[self.__current_account['USER_ID']],'TRADE_ID': TRADE_ID, 'POSTDATA': {}})
    
    @__validate
    def send_trade(self, TAG: str, TRADE_DATA: dict) -> dict:
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
        
        self.__ExecuteSequence(METHOD='SEND', INIT_DATA={'USER_ID': self.__accs[self.__current_account['USER_ID']], 'POSTDATA': TRADE_DATA})
        
        # XCSRF = self.__getXCSRF()
        
        # CHALLENGE_MD, CHALLENGE_ID, CHALLENGE_TYPE = self.__getChallengeID(XCSRF, TRADE_DATA, 1)
        
        # if not CHALLENGE_MD:
        #     return {'code': 1, 'msg': 'Trade did not need authorization'}

        # FINAL_CMD = self.__twoStep(XCSRF, CHALLENGE_MD)
        
        # r_accept = self.__current_session.post(url=f"https://trades.roblox.com/v1/trades/{5}/accept",headers={'rblx-challenge-id': CHALLENGE_ID,'rblx-challenge-metadata': FINAL_CMD,'rblx-challenge-type': CHALLENGE_TYPE,'x-csrf-token': XCSRF ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": self.__accs[self.__current_account['RBLX_COOKIE']]})
        # j = r_accept.json()
        # if r_accept.status_code == 200:
        #     return j
        # else:
        #     raise APIError(f'APIError for accept_trade:\n\n{r_accept.status_code}, {j}')
   
    @__validate
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
    
  
class TradeAuthenticatorAsync:
    """
    The *A*synchronous wrapper for TradeAuthenticator.

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
    
    async def __getXCSRF(self) -> str:
        """Private method. """
        get_token = await self.__current_session.post("https://auth.roblox.com/v2/logout",cookies={".ROBLOSECURITY": self.__accs[self.__current_account]['RBLX_COOKIE']})
        if get_token.status == 200:
            return get_token.headers["x-csrf-token"]
        else:
            j = get_token.json()
            raise APIError(f'APIError for __getXCSRF:\n\n{get_token.status}, {j}')
        
    async def __getChallengeID(self, XCSRF, TRADE_ID) -> str:
        """Private method. """
        r_init = await self.__current_session.post(url=f"https://trades.roblox.com/v1/trades/{TRADE_ID}/accept",headers={'x-csrf-token': XCSRF ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": self.__accs[self.__current_account]['RBLX_COOKIE']})
        if r_init.status == 200:
            return False,False,False
        elif r_init.status == 400 or r_init.status == 401:
            return json.loads(base64.b64decode(r_init.headers.get('rblx-challenge-metadata')).decode("UTF-8"))['challengeId'], r_init.headers.get('rblx-challenge-id'), r_init.headers.get('rblx-challenge-type')
        else:
            j = await r_init.json()
            raise APIError(f'APIError for __getChallengeID:\n\n{r_init.status}, {j}')
        
    async def __twoStep(self, XCSRF, CHALLENGE_MD) -> str:
        """Private method. """
        r_verify = await self.__current_session.post(url=f"https://twostepverification.roblox.com/v1/users/{self.__accs[self.__current_account['USER_ID']]}/challenges/authenticator/verify"
                ,headers={'x-csrf-token': XCSRF ,"Content-Type": "application/json"}
                ,cookies={".ROBLOSECURITY": self.__accs[self.__current_account['RBLX_COOKIE']]}
                ,data=json.dumps({
                    'actionType': "Generic",
                    'challengeId': CHALLENGE_MD,
                    'code': TradeAuthenticator.__secrTo6Digi(self.__accs[self.__current_account['OTP_SECRET']])
                }))
        
        if r_verify.status == 200:
            Verification_MetaData = {
                'verificationToken': r_verify.json()['verificationToken'],
                'rememberDevice': True,
                'challengeId': CHALLENGE_MD,
                'actionType': "Generic"
            }
            return base64.b64encode(json.dumps(Verification_MetaData).encode("UTF-8"))
        else:
            j = r_verify.json()
            raise APIError(f'APIError for __twoStep:\n\n{r_verify.status}, {j}')
        
    def add(self, USER_ID: str , OTP_SECRET: str, RBLX_COOKIE: str, TAG: str = None) -> dict:
        """
        Adds a new  account to the account cache.
        Can be called in other commands.
        
        :param str USER_ID: Roblox user ID to attach to the cached account.
        :param str OTP_SECRET: OTP Secret string (Check the GitHub for more info).
        :param str RBLX_COOKIE: Your _ROBLOSECURITY cookie.
        :param str TAG: [OPTIONAL] Add a tag to the added account to index it easily later and use its data. If TAG is left empty, its value will be the USER_ID .
        
        """
        _l = locals()
        _l.pop('self')
        Validate._types(_l)
        
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
        
        Validate._types(UPDATED_INFO)
        
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
    
    async def accept_trade(self, TAG: str, TRADE_ID: int) -> dict:
        """
        Accept a trade with the speficied account (through TAG) and the TRADE_ID of the trade that you want to accept.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param str TRADE_ID: Speaks for itself. Make sure its the valid one though :)     
        
        """
        if not self.__accs.get(TAG):
            raise KeyError(f'{TAG} does not exist in account cache.')
        
        async with aiohttp.ClientSession('http://httpbin.org') as self.__current_session:
            self.__current_account = TAG
            
            XCSRF = await self.__getXCSRF()
            
            CHALLENGE_MD, CHALLENGE_ID, CHALLENGE_TYPE = await self.__getChallengeID(XCSRF, TRADE_ID)
        
            if not CHALLENGE_MD:
                return {'code': 1, 'msg': 'Trade did not need authorization'}
            
            FINAL_CMD = await self.__twoStep(XCSRF, CHALLENGE_MD)
            
            r_accept = await self.__current_session.post(url=f"https://trades.roblox.com/v1/trades/{TRADE_ID}/accept",headers={'rblx-challenge-id': CHALLENGE_ID,'rblx-challenge-metadata': FINAL_CMD,'rblx-challenge-type': CHALLENGE_TYPE,'x-csrf-token': XCSRF ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": self.__accs[self.__current_account['RBLX_COOKIE']]})
            j = await r_accept.json()
            
            await self.__current_session.close()
            if r_accept.status == 200:
                return j
            else:
                raise APIError(f'APIError for accept_trade:\n\n{r_accept.status}, {j}')
    
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
