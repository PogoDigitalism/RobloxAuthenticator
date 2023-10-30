from typing import Union

class Config:
    URLCONFIG = {
        'CHALLENGEID':
            {
                'SEND': 'https://trades.roblox.com/v1/trades/send',
                'ACCEPT': 'https://trades.roblox.com/v1/trades/$TRADE_ID$/accept'
            },
        'TRADE':
            {
                'SEND': 'https://trades.roblox.com/v1/trades/send',
                'ACCEPT': 'https://trades.roblox.com/v1/trades/$TRADE_ID$/accept'
            }
    }
    
    HTTPCONFIG = {
        # $ = query var
        'XCSRF': {
            'METHOD': 'POST',
            'URL': "https://auth.roblox.com/v2/logout",
            'COOKIES': ['.ROBLOSECURITY'],
            # 'COOKIES': [],
            'HEADERS': [],
            'DATA': {},
            'STATUS': [200, 403],
            'RETURN_HEADERS': ["x-csrf-token"],
            'PROCESSING': None
        },
        'CHALLENGEID': {
            'METHOD': 'POST',
            'URL': None,
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type'],
            'DATA': {},
            'STATUS': [403],
            'RETURN_HEADERS': ["rblx-challenge-metadata", "rblx-challenge-id", "rblx-challenge-type"],
            'PROCESSING': [['_getMetaDataChallengeId'],['challengeId']]
        },
        'TWOSTEP': {
            'METHOD': 'POST',
            'URL': "https://twostepverification.roblox.com/v1/users/$USER_ID$/challenges/authenticator/verify",
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type'],
            'DATA': {'actionType': 'actionType',
                     'challengeId': 'challengeId',
                     'code': 'OTP_SECRET'},
            'STATUS': [200],
            'RETURN_HEADERS' : [],
            'PROCESSING': [['_prepareMetaData','_rawMetaData'],['rblx-challenge-metadata','challengeMetadata']]
        },
        'CONTINUE': {
            'METHOD': 'POST',
            'URL': "https://apis.roblox.com/challenge/v1/continue",
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type'],
            'DATA': {'challengeId': 'rblx-challenge-id',
                     'challengeMetadata': 'challengeMetadata',
                     'challengeType': 'rblx-challenge-type'},
            'STATUS': [200],
            'RETURN_HEADERS' : [],
            'PROCESSING': None
        },
        # rblx-challenge-id': CHALLENGE_ID,'rblx-challenge-metadata': FINAL_CMD,'rblx-challenge-type': CHALLENGE_TYPE,'x-csrf-token': XCSRF ,"Content-Type": "application/json
        'TRADE': {
            'METHOD': 'POST',
            'URL': None,
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type', "rblx-challenge-metadata", "rblx-challenge-id", "rblx-challenge-type"],
            'DATA': 'SEND',
            'STATUS': [200],
            'RETURN_HEADERS' : [],
            'PROCESSING': None
        },
    }
    
    SEQUENCECONFIG = {
        'SEND': ['XCSRF', 'CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'TRADE'],
        'ACCEPT': ['XCSRF', 'CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'TRADE'],       
    }

    METHOD_ARGS =  {
        'add': ['USER_ID', 'OTP_SECRET', 'RBLX_COOKIE', 'TAG'],
        'config': ['TAG', 'UPDATED_INFO'],
        'remove': ['TAG'],
        'accept_trade': ['TAG', 'TRADE_ID'],
        'send_trade': ['TAG', 'TRADE_DATA'],
        'TradeData': ['SENDER_USER_ID', 'TRADE_RECIPIENT_USER_ID', 'OFFER', 'REQUEST', 'ROBUX', 'RECIPIENT_ROBUX']
    }
    
    VALIDATE_TYPES = {'USER_ID': Union[str, int],
                  'OTP_SECRET': str,
                  'RBLX_COOKIE': str,
                  'TAG': str,
                  
                  'TRADE_DATA': dict,
                  'TRADE_ID': int,
                  'OFFER': list,
                  'REQUEST': list,
                  
                  'TRADE_RECIPIENT_USER_ID': Union[str, int],
                  'SENDER_USER_ID': int,
                  'RECIPIENT_ROBUX': int,
                  'ROBUX': int}
    
    
    @classmethod
    def _Sequence(cls, METHOD: str) -> dict:
        return cls.SEQUENCECONFIG[METHOD]
