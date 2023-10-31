
# Roblox Mobile Authenticator
by PogoDigitalism (Same username on Discord)

🎉 Easily authenticate your HTTP Requests with **RobloxMobileAuthenticator**! 🎉


## This tool provides automation of group payouts and trades!
This is an easy-to-use wrapper written in 100% Python to automate process of Roblox' **2FA MOBILE authentication** system.
RobloxMobileAuthenticator contains both a synchronous and asynchronous way of making these requests!


    ⚠️ This library requires the external pyotp, requests and aiohttp libraries to function. ⚠️

### A small introduction:
Check out [this](https://github.com/PogoDigitalism/RobloxMobileAuthenticator/blob/main/examples/sending_trades.py) for examples on how to use this lib.

In order for RobloxMobileAuthenticator to make succesful HTTP requests, it requires a Roblox account's TOTP secret (to generate a 6-digit code) and .ROBLOSECURITY (to authorize requests).
Below is a tutorial that shows how to get this TOTP as it is a bit hidden in your account settings.

### TOTP KEY TUTORIAL:
To get the key, go to Roblox privacy settings, reset/add mobile authentication.

![image](https://github.com/PogoDigitalism/RobloxTradeAuthenticator/assets/107322523/2a448f61-3781-475e-880f-ed3a7cfc95c9)

Then, click the 'Cant't scan the code? Click here for manual entry'
This is your secret key (OTP_SECRET). Copy and paste this in your code (You can share this code across multiple devices, so adding this to your phone won't affect your program.
