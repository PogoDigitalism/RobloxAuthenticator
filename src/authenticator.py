import requests
import aiohttp
import config
from exceptions import APIError, AlreadyProcessedError
from utils import Validate, privUtils
from typing import Union
import json

class _Profile: #Kind of redundant, added for code readibility
    def __init__(self, otp, ck, i_d) -> None:
        self.OTP_SECRET = otp
        self.RBLX_COOKIE = ck
        self.USER_ID = i_d


class Authenticator:
    """
    The synchronous wrapper for TradeAuthenticator.

    Please read the GitHub for all info that you need.
    https://github.com/PogoDigitalism/RobloxMobileAuthenticator/
    
    """  
    def __init__(self) -> None:
        self._accs: dict[str, dict[str,int]] = dict()
        self.__current_account = str()
        self.__current_session: requests.Session()
    
    def __ExecuteSequence(self, **kwargs): #Main sequence
        METHOD = kwargs['METHOD']
        INIT_DATA: dict = kwargs['INIT_DATA']
        varDict = {'Content-Type': 'application/json', 'actionType': 7}
        varDict['.ROBLOSECURITY'] = self._accs[self.__current_account]['RBLX_COOKIE']
        
        SEQUENCE = config.Config._Sequence(METHOD)
        
        resp: requests.Response
        for httpMethod in SEQUENCE:
            methodInfo = config.Config.HTTPCONFIG[httpMethod]
            
            methodHeaders = methodInfo['HEADERS']
            headersSubmit = {}
            for h in methodHeaders:
                headersSubmit[h] = varDict[h]
                
            methodData = methodInfo['DATA']
            if not isinstance(methodData, str):
                varDict['OTP_SECRET'] = privUtils._secrTo6Digi(self._accs[self.__current_account]['OTP_SECRET']) #Stores the generated 6-Digit code in OTP_SECRET
                dataSubmit = {}
                for d in methodData:
                    dataSubmit[d] = varDict[methodData[d]]
            else:
                dataSubmit = kwargs['INIT_DATA']['POSTDATA'] #In other words, if it's time to apply the passed initial method data (trade data, payout data), then set dataSubmit to that
                
            methodCookies = methodInfo['COOKIES']
            cookiesSubmit = {}
            for c in methodCookies:
                cookiesSubmit[c] = varDict[c]

            if not methodInfo['URL']:
                url = config.Config.URLCONFIG[httpMethod][METHOD]
            else:
                url = methodInfo['URL']
            url = privUtils._urlProcessing(INIT_DATA, url) # private utility function to replace $VAR_NAME$ in the links with VAR_NAME's value

            if methodInfo['METHOD'] == 'POST':
                resp = self.__current_session.post(url, data=json.dumps(dataSubmit), headers=headersSubmit, cookies=cookiesSubmit)
            elif methodInfo['METHOD'] == 'GET':
                resp = self.__current_session.get(url, data=json.dumps(dataSubmit), headers=headersSubmit, cookies=cookiesSubmit)
           
            if resp.status_code in methodInfo['STATUS']:
                for respHeader in methodInfo['RETURN_HEADERS']:   
                    varDict[respHeader] = resp.headers.get(respHeader) #Get required headers and store them in VAR_DICT

                if methodInfo['PROCESSING']:
                    for i, funcs in enumerate(methodInfo['PROCESSING'][0]): # Loops through all methods required to process the response of the HTTP request
                        varDict[methodInfo['PROCESSING'][1][i]] = getattr(privUtils, methodInfo['PROCESSING'][0][i])(resp, varDict) 
            else: #You want to catch these Exceptions in your main code
                if resp.status_code == 200:
                    raise AlreadyProcessedError('No authentication needed.')
                else:
                    raise APIError(f'HTTP Request failed\n\n{resp.status_code}: {resp.json()}')
            
        self.__current_session.close()
        return resp  

    @Validate.validate_types
    def add(self, USER_ID: Union[str, int], OTP_SECRET: str, RBLX_COOKIE: str, TAG: str = None) -> dict:
        """
        Adds a new  account to the account cache.
        Can be called in other commands.
        
        :param str USER_ID: Roblox user ID to attach to the cached account.
        :param str OTP_SECRET: OTP Secret string (Check the GitHub for more info).
        :param str RBLX_COOKIE: Your _ROBLOSECURITY cookie.
        :param str TAG: [OPTIONAL] Add a tag to the added account to index it easily later and use its data. If TAG is left empty, its value will be the USER_ID .
        
        """
        if not TAG:
            TAG = USER_ID

        accountData: dict = _Profile(OTP_SECRET, RBLX_COOKIE, int(USER_ID)).__dict__
        self._accs[TAG] = accountData
        return accountData

    @Validate.validate_tag   
    @Validate.validate_types
    def config(self, TAG: str, UPDATED_INFO: dict[str, str]) -> dict:
        """
        Configure a cached account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        :param dict UPDATED_INFO: Invalid key value pairs will raise a *KeyError* or *NotImplementedError*.
        
        """
        for _k in UPDATED_INFO:
            self._accs[TAG][_k] = UPDATED_INFO[_k]
            
        return self._accs[TAG]

    @Validate.validate_tag   
    @Validate.validate_types
    def remove(self, TAG: str) -> bool:
        """
        Remove an account from the cache.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        
        """
        self._accs.pop(TAG)

    @Validate.validate_tag   
    @Validate.validate_types
    def accept_trade(self, TAG: str, TRADE_ID: int) -> requests.Response:
        """
        Accept a trade with the speficied account (through TAG) and the TRADE_ID of the trade that you want to accept.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param str TRADE_ID: Speaks for itself. Make sure its the valid one though :)     
        
        """

        
        self.__current_account = TAG
        self.__current_session = requests.session()
        
        return self.__ExecuteSequence(METHOD='ACCEPT', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'TRADE_ID': TRADE_ID, 'POSTDATA': {}})

    @Validate.validate_tag   
    @Validate.validate_types
    def send_trade(self, TAG: str, TRADE_DATA: dict) -> requests.Response:
        """
        Send a trade with the speficied account (through TAG) and the TRADE_DATA of the trade.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param str TRADE_DATA: Speaks for itself. You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling TradeData to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = requests.session()
        
        return self.__ExecuteSequence(METHOD='SEND', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'], 'POSTDATA': TRADE_DATA})

    @Validate.validate_tag   
    @Validate.validate_types
    def one_time_payout(self, TAG: str, GROUP_ID: int, PAYOUT_DATA: dict) -> requests.Response:
        """
        Pay out a group member for a single time with Robux. 
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param int GROUP_ID: Speaks for itself. Make sure its the valid one though :)    
        :param dict PAYOUT_DATA: You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling OneTimePayout to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = requests.Session()
        
        return self.__ExecuteSequence(METHOD='GROUP_ONE_TIME_PAYOUT', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'GROUP_ID': GROUP_ID, 'POSTDATA': PAYOUT_DATA})

    @Validate.validate_tag   
    @Validate.validate_types
    def recurring_payout(self, TAG: str, GROUP_ID: int, PAYOUT_DATA: dict) -> requests.Response:
        """
        Create a recurring payout in the form of a percentage of the total group funds (this is built-in in Roblox' API). 
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param int GROUP_ID: Speaks for itself. Make sure its the valid one though :)    
        :param dict PAYOUT_DATA: You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling RecurringPayout to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = requests.Session()
        
        return self.__ExecuteSequence(METHOD='GROUP_RECURRING_PAYOUT', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'GROUP_ID': GROUP_ID, 'POSTDATA': PAYOUT_DATA})

    @Validate.validate_tag   
    @Validate.validate_types
    def accessory_purchase(self, TAG: str, ACCESSORY_ID: int, PURCHASE_DATA: dict) -> requests.Response:
        """
        Create a recurring payout in the form of a percentage of the total group funds (this is built-in in Roblox' API). 
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param int SELLER_ID: Speaks for itself, can be a group or user ID. Make sure its the valid one though :)    
        :param dict PURCHASE_DATA: You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling AccessoryPurchase to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = requests.Session()
        
        return self.__ExecuteSequence(METHOD='ACCESSORY_PURCHASE', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'ACCESSORY_ID': ACCESSORY_ID, 'POSTDATA': PURCHASE_DATA})
 
    @Validate.validate_tag          
    @Validate.validate_types
    def info(self, TAG: str) -> dict:
        """
        Get the data of an account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        
        """
        if self._accs.get(TAG):
            return self._accs[TAG]
        raise KeyError(f'{TAG} does not exist in account cache.')
    
    def __repr__(self) -> str:
        return f'CLASS REPR: {self._accs}'
 
  
class AuthenticatorAsync:
    """
    The *A*synchronous wrapper for TradeAuthenticator.

    Please read the GitHub for all info that you need.
    https://github.com/PogoDigitalism/RobloxMobileAuthenticator/
    
    """
    def __init__(self) -> None:
        self._accs: dict[str, dict[str,int]] = dict()
        self.__current_account = str()
        self.__current_session: aiohttp.ClientSession()
    
    async def __ExecuteSequence(self, **kwargs):
        METHOD = kwargs['METHOD']
        INIT_DATA: dict = kwargs['INIT_DATA']
        varDict = {'Content-Type': 'application/json', 'actionType': 7}
        varDict['.ROBLOSECURITY'] = self._accs[self.__current_account]['RBLX_COOKIE']
        
        SEQUENCE = config.Config._Sequence(METHOD)

        for httpMethod in SEQUENCE:
            methodInfo = config.Config.HTTPCONFIG[httpMethod]
            
            methodHeaders = methodInfo['HEADERS']
            headersSubmit = {}
            for h in methodHeaders:
                headersSubmit[h] = varDict[h]
                
            methodData = methodInfo['DATA']
            if not isinstance(methodData, str):
                varDict['OTP_SECRET'] = privUtils._secrTo6Digi(self._accs[self.__current_account]['OTP_SECRET'])
                dataSubmit = {}
                for d in methodData:
                    dataSubmit[d] = varDict[methodData[d]]
            else:
                dataSubmit = kwargs['INIT_DATA']['POSTDATA']
                
            methodCookies = methodInfo['COOKIES']
            cookiesSubmit = {}
            for c in methodCookies:
                cookiesSubmit[c] = varDict[c]

            if methodInfo['URL'] is None:
                url = config.Config.URLCONFIG[httpMethod][METHOD]
            else:
                url = methodInfo['URL']
            url = privUtils._urlProcessing(INIT_DATA, url)

            if methodInfo['METHOD'] == 'POST':
                resp = await self.__current_session.post(url, data=json.dumps(dataSubmit), headers=headersSubmit, cookies=cookiesSubmit)
            elif methodInfo['METHOD'] == 'GET':
                resp = await self.__current_session.get(url, data=json.dumps(dataSubmit), headers=headersSubmit, cookies=cookiesSubmit)
           
            if resp.status_code in methodInfo['STATUS']:
                for respHeader in methodInfo['RETURN_HEADERS']:   
                    varDict[respHeader] = resp.headers.get(respHeader)

                if methodInfo['PROCESSING']:
                    for i, funcs in enumerate(methodInfo['PROCESSING'][0]):
                        varDict[methodInfo['PROCESSING'][1][i]] = getattr(privUtils, methodInfo['PROCESSING'][0][i])(resp, varDict)
            else:
                if resp.status_code == 200:
                    raise AlreadyProcessedError('No authentication needed.')
                else:
                    raise APIError(f'HTTP Request failed\n\n{resp.status_code}: {resp.json()}')
            
        self.__current_session.close()
        return resp
        
    @Validate.validate_types
    def add(self, USER_ID: Union[str, int] , OTP_SECRET: str, RBLX_COOKIE: str, TAG: str = None) -> dict:
        """
        Adds a new  account to the account cache.
        Can be called in other commands.
        
        :param str USER_ID: Roblox user ID to attach to the cached account.
        :param str OTP_SECRET: OTP Secret string (Check the GitHub for more info).
        :param str RBLX_COOKIE: Your _ROBLOSECURITY cookie.
        :param str TAG: [OPTIONAL] Add a tag to the added account to index it easily later and use its data. If TAG is left empty, its value will be the USER_ID .
        
        """
        if not TAG:
            TAG = USER_ID
        
        accountData: dict = _Profile(OTP_SECRET, RBLX_COOKIE, int(USER_ID)).__dict__
        self._accs[TAG] = accountData
        return accountData

    @Validate.validate_tag   
    @Validate.validate_types
    def config(self, TAG: str, UPDATED_INFO: dict[str, str]) -> dict:
        """
        Configure a cached account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        :param dict UPDATED_INFO: Invalid key value pairs will raise a *KeyError* or *NotImplementedError*.
        
        """
        for _k in UPDATED_INFO:
            self._accs[TAG][_k] = UPDATED_INFO[_k]
            
        return self._accs[TAG]

    @Validate.validate_tag   
    @Validate.validate_types
    def remove(self, TAG: str) -> bool:
        """
        Remove an account from the cache.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        
        """
        if self._accs.get(TAG):
            self._accs.pop(TAG)
            return True
        raise KeyError(f'{TAG} does not exist in account cache.')    

    @Validate.validate_tag   
    @Validate.validate_types
    async def accept_trade(self, TAG: str, TRADE_ID: int) -> aiohttp.ClientResponse:
        """
        Accept a trade with the speficied account (through TAG) and the TRADE_ID of the trade that you want to accept.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param str TRADE_ID: Speaks for itself. Make sure its the valid one though :)     
        
        """

        
        self.__current_account = TAG
        self.__current_session = aiohttp.ClientSession()
        
        return await self.__ExecuteSequence(METHOD='ACCEPT', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'TRADE_ID': TRADE_ID, 'POSTDATA': {}})
  
    @Validate.validate_tag   
    @Validate.validate_types
    async def send_trade(self, TAG: str, TRADE_DATA: dict) -> aiohttp.ClientResponse:
        """
        Send a trade with the speficied account (through TAG) and the TRADE_DATA of the trade.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param str TRADE_DATA: Speaks for itself. You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling TradeData to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = aiohttp.ClientSession()
        
        await self.__ExecuteSequence(METHOD='SEND', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'], 'POSTDATA': TRADE_DATA})

    @Validate.validate_tag   
    @Validate.validate_types
    async def one_time_payout(self, TAG: str, GROUP_ID: int, PAYOUT_DATA: dict) -> aiohttp.ClientResponse:
        """
        Pay out a group member for a single time with Robux. 
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param int GROUP_ID: Speaks for itself. Make sure its the valid one though :)    
        :param dict PAYOUT_DATA: You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling OneTimePayout to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = aiohttp.ClientSession()
        
        return await self.__ExecuteSequence(METHOD='GROUP_ONE_TIME_PAYOUT', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'GROUP_ID': GROUP_ID, 'POSTDATA': PAYOUT_DATA})

    @Validate.validate_tag   
    @Validate.validate_types
    async def recurring_payout(self, TAG: str, GROUP_ID: int, PAYOUT_DATA: dict) -> aiohttp.ClientResponse:
        """
        Create a recurring payout in the form of a percentage of the total group funds (this is built-in in Roblox' API). 
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param int GROUP_ID: Speaks for itself. Make sure its the valid one though :)    
        :param dict PAYOUT_DATA: You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling RecurringPayout to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = aiohttp.ClientSession()
        
        return await self.__ExecuteSequence(METHOD='GROUP_RECURRING_PAYOUT', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'GROUP_ID': GROUP_ID, 'POSTDATA': PAYOUT_DATA})
    
    @Validate.validate_tag    
    @Validate.validate_types
    async def accessory_purchase(self, TAG: str, ACCESSORY_ID: int, PURCHASE_DATA: dict) -> requests.Response:
        """
        Create a recurring payout in the form of a percentage of the total group funds (this is built-in in Roblox' API). 
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        :param int SELLER_ID: Speaks for itself, can be a group or user ID. Make sure its the valid one though :)    
        :param dict PURCHASE_DATA: You can easily format your data into a valid TRADE_DATA entry using
        importing Formatting from utils and calling AccessoryPurchase to get a formatted dictionairy.  
        
        """

        
        self.__current_account = TAG
        self.__current_session = requests.Session()
        
        return await self.__ExecuteSequence(METHOD='ACCESSORY_PURCHASE', INIT_DATA={'USER_ID': self._accs[self.__current_account]['USER_ID'],'ACCESSORY_ID': ACCESSORY_ID, 'POSTDATA': PURCHASE_DATA})
    
    @Validate.validate_tag   
    @Validate.validate_types
    def info(self, TAG: str) -> dict:
        """
        Get the data of an account.
        
        :param str TAG: Use USER_ID's value for TAG if you did not assign a TAG when creating the account that you want to use.
        Will raise a *KeyError* if the TAG does not exist in the cache.
        
        """
        if self._accs.get(TAG):
            return self._accs[TAG]
        raise KeyError(f'{TAG} does not exist in account cache.')
    
    def __repr__(self) -> str:
        return f'CLASS REPR: {self._accs}'
