import base64
import json
import ast
import pyotp
# Credits to KeyNodes for showing how he decoded the metadata and got the actual required challengeId

# I did not add any Exception catching in this code. I also did not optimise this code (there is not much to optimise about this though)
def accept_trade(cookie,trade_id,OTP_SECRET,user_id):
    s = requests.session()
    
    get_token = s.post("https://auth.roblox.com/v2/logout",cookies={".ROBLOSECURITY": cookie})
    xcsrf_token = get_token.headers["x-csrf-token"]

    r_init = s.post(url=f"https://trades.roblox.com/v1/trades/{trade_id}/accept",headers={'x-csrf-token': xcsrf_token ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": cookie})
    
    # Get the challenge Id required to get the verificationToken from the twostepverification api. This challenge Id is hidden in the metadata (for some reason)
    challengeId_fromMetaData = json.loads(base64.b64decode(r_init.headers.get('rblx-challenge-metadata')).decode("UTF-8"))['challengeId']

    r_verify = s.post(url=f"https://twostepverification.roblox.com/v1/users/{user_id}/challenges/authenticator/verify"
            ,headers={'x-csrf-token': xcsrf_token ,"Content-Type": "application/json"}
            ,cookies={".ROBLOSECURITY": cookie}
            ,data=json.dumps({
                'actionType': "Generic",
                'challengeId': challengeIdMetaData,
                'code': pyotp.TOTP("OTP_SECRET").now()
            }))
    
    Verification_MetaData = {
        'verificationToken': r_verify.json()['verificationToken'],
        'rememberDevice': True,
        'challengeId': challengeId_fromMetaData,
        'actionType': "Generic"
    }
    Verification_MetaData = base64.b64encode(json.dumps(Verification_MetaData).encode("UTF-8"))

    init_challengeId = r_init.headers.get('rblx-challenge-id')
    init_challengeType = r_init.headers.get('rblx-challenge-type')
    r_accept = s.post(url=f"https://trades.roblox.com/v1/trades/{trade_id}/accept",headers={'rblx-challenge-id': init_challengeId,'rblx-challenge-metadata': challengeId_fromMetaData,'rblx-challenge-type': init_challengeType,'x-csrf-token': xcsrf_token ,"Content-Type": "application/json"},cookies={".ROBLOSECURITY": cookie})

    return r_accept.json(),r_accept.status_code
 

ROBLOSEC = 'your ROBLOSECURITY cookie here'

# trade_id and user_id are both integers. Replace the whole string with your id integers.
trade_id = 'whatever trade id your bot needs to authenticate'
user_id = 'your roblox account user id'

#you can get OTP SECRET by enabling Authenticator App in privacy settings (Roblox) and clicking 'Can't scan the QR code?'. Copy the manual entry and paste it in OTP_SECRET, do not share this with anyone.
OTP_SECRET = 'your OPT SECRET'

accept_trade(ROBLOSEC,trade_id,OTP_SECRET,user_id)
