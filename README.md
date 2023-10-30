# Roblox Trade Authenticator


Supports synchronous and asynchronous code
## This wrapper currently only provides ACCEPTING and SENDING trades, additional features will be added in the future.
This is an easy-to-use wrapper written in 100% Python to combat Roblox' new **2FA MOBILE authentication** system. Contains both a synchronous and asynchronous class with methods.

You need:
 - Roblox trade ID (will probably be a dynamic variable in your code)
 - Roblox user ID (constant/variable)
 - ROBLOSECURITY cookie (for authorization)
 - Secret Key for TOTP (tutorial below)


This library requires the external pyotp, requests and aiohttp libraries to function. 

**To contact me:**
PogoDigitalism on Discord


### TOTP KEY TUTORIAL:
To get the key, go to Roblox privacy settings, reset/add mobile authentication.

![image](https://github.com/PogoDigitalism/RobloxTradeAuthenticator/assets/107322523/2a448f61-3781-475e-880f-ed3a7cfc95c9)

Then, click the 'Cant't scan the code? Click here for manual entry'
This is your secret key (OTP_SECRET). Copy and paste this in your code (You can share this code across multiple devices, so adding this to your phone won't affect your program.
