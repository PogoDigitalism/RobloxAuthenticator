import aiohttp 
import requests
from typing import Union
import pyotp
import json
import base64
import config

class privUtils:
    def _getMetaDataChallengeId(resp: Union[requests.Response, aiohttp.ClientResponse], VAR_DICT: dict):
        """Private method. """
        return json.loads(base64.b64decode(resp.headers.get('rblx-challenge-metadata')).decode("UTF-8"))['challengeId']

    def _prepareMetaData(resp: Union[requests.Response, aiohttp.ClientResponse], VAR_DICT: dict):
        """Private method. """
        Verification_MetaData = {
                    'verificationToken': resp.json()['verificationToken'],
                    'rememberDevice': True,
                    'challengeId': VAR_DICT['challengeId'],
                    'actionType': "Generic"
                }
        return base64.b64encode(json.dumps(Verification_MetaData).encode("UTF-8"))

    def _rawMetaData(resp: Union[requests.Response, aiohttp.ClientResponse], VAR_DICT: dict):
        """Private method. """
        Verification_MetaData = {
                    'verificationToken': resp.json()['verificationToken'],
                    'rememberDevice': True,
                    'challengeId': VAR_DICT['challengeId'],
                    'actionType': "Generic"
                }
        return json.dumps(Verification_MetaData)

    def _secrTo6Digi(OTP_SECRET: str) -> str:
        """Private method. """
        return str(pyotp.TOTP(OTP_SECRET).now())
    
    def _urlProcessing(INIT_DATA: dict, url: str) -> str:
        if '$' in url:
            var = INIT_DATA.get(url.split('$')[1])
            url = url.replace(f"${url.split('$')[1]}$", str(var))
        return url
    
class Validate:
    @staticmethod
    def validate_types(func):
        def wrapper(*args, **kwargs):
            Validate._types(*args, **kwargs, funcname = func.__name__)

            result = func(*args, **kwargs)
            return result
        return wrapper
    
    @staticmethod
    def _types(*args, **kwargs) -> bool | None:
        """Private method. """
        
        args = list(args)
        if 'CLASS' in str(args[0]): 
            args.pop(0)
            
        _locals = {}
        for i, arg in enumerate(args):
            _locals[config.Config.METHOD_ARGS[kwargs['funcname']][i]] = arg        
        for kwarg in kwargs:
            _locals[kwarg] = kwargs[kwarg]
        _locals.pop('funcname')
            
        for _k in _locals:
            if not _locals.get(_k):
                raise KeyError(f'{_k} is not a valid keyword argument.')

            if not isinstance(_locals[_k], config.Config.VALIDATE_TYPES[_k]):
                raise TypeError(f'Invalid type "{type(_locals[_k])}" for {_k}.\n\n--> Use the proper types that are hinted.')

        return True

class Formatting:
    @staticmethod
    @Validate.validate_types
    def TradeData(SENDER_USER_ID: Union[str, int], TRADE_RECIPIENT_USER_ID: Union[str, int], OFFER: list, REQUEST: list, ROBUX: int = 0, RECIPIENT_ROBUX: int = 0) -> dict[str, dict[str, Union[list, int]]]:
        """Formats your data into a dictionairy that can be used for sending and countering trades."""
        return {
        "offers": [
            {
            "userId": int(SENDER_USER_ID),
            "userAssetIds": OFFER,
            "robux": abs(ROBUX)
            },
            {
            "userId": int(TRADE_RECIPIENT_USER_ID),
            "userAssetIds": REQUEST,
            "robux": abs(RECIPIENT_ROBUX)
        }
            ]
        }
    
    def __repr__(self) -> str:
        return f'CLASS'
