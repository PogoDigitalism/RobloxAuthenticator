# Roblox Trade Authenticator
 ⚠️ REPO IS CURRENTLY IN OVERHAUL, DON'T USE IT 1:1 AS OF RIGHT NOW. ⚠️

(instead, copy the methods that I am using for authentication.)





Supports synchronous and asynchronous code
## This wrapper currently only provides ACCEPTING trades, additional features will be added in the future.
This is a simple wrapper written for Python to combat Roblox' new **2FA MOBILE authentication** system. Contains both a synchronous and asynchronous class with methods.

You need:
 - Roblox trade ID (will probably be a dynamic variable in your code)
 - Roblox user ID (constant/variable)
 - ROBLOSECURITY cookie (for authorization)
 - Secret Key for TOTP (tutorial below)

TradeAuthenticator.py contains the source.

This function requires the external pyotp, requests and aiohttp libraries to function. 

**To contact me:**
PogoDigitalism on Discord


### TOTP KEY TUTORIAL:
To get the key, go to Roblox privacy settings, reset/add mobile authentication.

Then, click the 'Cant't scan the code? Click here for manual entry'
![image](https://github.com/PogoDigitalism/RobloxTradeAuthenticator/assets/107322523/2a448f61-3781-475e-880f-ed3a7cfc95c9)

This is your secret key (OTP_SECRET). Copy and paste this in your code (You can share this code across multiple devices, so adding this to your phone won't affect your program.
