from typing import Union

class Config:
    """Do not mess with the configs unless you know what you're doing!"""
    URLCONFIG = {
        'CHALLENGEID':
            {
                'SEND': 'https://trades.roblox.com/v1/trades/send',
                'ACCEPT': 'https://trades.roblox.com/v1/trades/$TRADE_ID$/accept'
            },
        'GROUP_CHALLENGEID':
            {
                'GROUP_ONE_TIME_PAYOUT': 'https://groups.roblox.com/v1/groups/$GROUP_ID$/payouts',
                'GROUP_RECURRING_PAYOUT': 'https://groups.roblox.com/v1/groups/$GROUP_ID$/payouts/recurring'
            },
        'TRADE':
            {
                'SEND': 'https://trades.roblox.com/v1/trades/send',
                'ACCEPT': 'https://trades.roblox.com/v1/trades/$TRADE_ID$/accept',
                'DECLINE': 'https://trades.roblox.com/v1/trades/$TRADE_ID$/decline',
                'COUNTER': 'https://trades.roblox.com/v1/trades/$TRADE_ID$/counter'
            },
        'GROUP':
            {
                'GROUP_ONE_TIME_PAYOUT': 'https://groups.roblox.com/v1/groups/$GROUP_ID$/payouts',
                'GROUP_RECURRING_PAYOUT': 'https://groups.roblox.com/v1/groups/$GROUP_ID$/payouts/recurring'
            }
    }
    
    HTTPCONFIG = {
        # $ = query var
        'XCSRF': {
            'METHOD': 'POST',
            'URL': "https://auth.roblox.com/v2/logout",
            'COOKIES': ['.ROBLOSECURITY'],
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
            'DATA': 'TRADE',
            'STATUS': [403],
            'RETURN_HEADERS': ["rblx-challenge-metadata", "rblx-challenge-id", "rblx-challenge-type"],
            'PROCESSING': [['_getMetaDataChallengeId'],['challengeId']]
        },
        'GROUP_CHALLENGEID': {
            'METHOD': 'POST',
            'URL': None,
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type'],
            'DATA': 'GROUP',
            'STATUS': [403],
            'RETURN_HEADERS': ["rblx-challenge-metadata", "rblx-challenge-id", "rblx-challenge-type"],
            'PROCESSING': [['_getMetaDataChallengeId'],['challengeId']]
        },
        'PURCHASE_CHALLENGEID': {
            'METHOD': 'POST',
            'URL': 'https://economy.roblox.com/v1/purchases/products/$ACCESSORY_ID$',
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type'],
            'DATA': 'PURCHASE',
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
        # rblx-challenge-id': CHALLENGE_ID,'rblx-challenge-metadata': FINAL_CMD,'rblx-challenge-type': CHALLENGE_TYPE,'x-csrf-token': XCSRF ,"Content-Type": "application/json
        'GROUP': {
            'METHOD': 'POST',
            'URL': None,
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type', "rblx-challenge-metadata", "rblx-challenge-id", "rblx-challenge-type"],
            'DATA': 'PAYOUT',
            'STATUS': [200],
            'RETURN_HEADERS' : [],
            'PROCESSING': None
        },
        'PURCHASE': {
            'METHOD': 'POST',
            'URL': 'https://economy.roblox.com/v1/purchases/products/$ACCESSORY_ID$',
            'COOKIES': ['.ROBLOSECURITY'],
            'HEADERS': ['x-csrf-token', 'Content-Type'],
            'DATA': 'PURCHASE',
            'STATUS': [200],
            'RETURN_HEADERS' : [],
            'PROCESSING': None
        },
    }
        
    SEQUENCECONFIG = {
        'SEND': ['XCSRF', 'CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'TRADE'],
        'ACCEPT': ['XCSRF', 'CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'TRADE'],
        'DECLINE': ['XCSRF', 'CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'TRADE'],
        'COUNTER': ['XCSRF', 'CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'TRADE'],
        
        'GROUP_ONE_TIME_PAYOUT': ['XCSRF', 'GROUP_CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'GROUP'],
        'GROUP_RECURRING_PAYOUT': ['XCSRF', 'GROUP_CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'GROUP'],

        'ACCESSORY_PURCHASE': ['XCSRF', 'PURCHASE_CHALLENGEID', 'TWOSTEP', 'CONTINUE', 'PURCHASE']    
    }

    METHOD_ARGS =  {
        'add': ['USER_ID', 'OTP_SECRET', 'RBLX_COOKIE', 'TAG'],
        'config': ['TAG', 'UPDATED_INFO'],
        'remove': ['TAG'],
        'accept_trade': ['TAG', 'TRADE_ID'],
        'send_trade': ['TAG', 'TRADE_DATA'],
        'decline_trade': ['TAG', 'TRADE_ID'],
        'counter_trade': ['TAG', 'TRADE_ID','TRADE_DATA'],
        'one_time_payout': ['TAG', 'GROUP_ID', 'PAYOUT_DATA'],
        'recurring_payout': ['TAG', 'GROUP_ID', 'PAYOUT_DATA'],
        'accessory_purchase': ['TAG', 'ACCESSORY_ID', 'PURCHASE_DATA'],
        'TradeData': ['SENDER_USER_ID', 'TRADE_RECIPIENT_USER_ID', 'OFFER', 'REQUEST', 'ROBUX', 'RECIPIENT_ROBUX'],
        'OneTimePayout': ['PAYOUT_RECIPIENT_USER_ID', 'ROBUX'],
        'RecurringPayout': ['PAYOUT_RECIPIENT_USER_ID', 'PERCENTAGE'],
        'AccessoryPurchase': ['PRICE', 'SELLER_ID'],
    }
    
    VALIDATE_TYPES = {'USER_ID': Union[str, int],
                  'OTP_SECRET': str,
                  'RBLX_COOKIE': str,
                  'TAG': str,
                  
                  'TRADE_DATA': dict,
                  'TRADE_ID': int,
                  'OFFER': list,
                  'REQUEST': list,
                  'PAYOUT_RECIPIENT_USER_ID': int,
                  'GROUP_ID': int,
                  'PAYOUT_DATA': dict,
                  'PURCHASE_DATA': dict,
                  'PERCENTAGE': int,
                  'ACCESSORY_ID': int,
                  'SELLER_ID': int,
                  'PRICE': int,
                  
                  'TRADE_RECIPIENT_USER_ID': Union[str, int],
                  'SENDER_USER_ID': int,
                  'RECIPIENT_ROBUX': int,
                  'ROBUX': int}
    
    
    @classmethod
    def _Sequence(cls, METHOD: str) -> dict:
        return cls.SEQUENCECONFIG[METHOD]
