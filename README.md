
# Roblox Authenticator
### by PogoDigitalism (contact me on Discord <img src="https://i.pinimg.com/736x/79/94/28/7994282748b571ed81197ed915d998ea.jpg" width="22" height="22">)

🎉 Easily authenticate your HTTP Requests with **RobloxAuthenticator**! 🎉


## This tool provides automation of group payouts, asset purchases (not thoroughly tested) and trades!
This is an easy-to-use wrapper written in 100% Python to automate process of Roblox' **2FA MOBILE authentication** system.
RobloxAuthenticator contains both a synchronous and asynchronous way of making these requests!

`❗ This is **NOT** a 2FA bypasser and can not be used to gain unauthorized access to Roblox accounts. I strongly discourage account theft and any other malicious practices of such matter.
This library is therefore not made and compatible to be used as account stealer. RobloxAuthenticator is simply for enthusiastic people like me who want to make their life easier, make cool stuff and do good for others.`


    ⚠️ RobloxAuthenticator requires the external pyotp, requests and aiohttp (only for asynchronous methods) libraries to function. ⚠️

### A small introduction:
Check out [this](https://github.com/PogoDigitalism/RobloxAuthenticator/tree/main/examples) for examples on how to use RobloxAuthenticator.

In order for RobloxAuthenticator to make succesful HTTP requests, it requires a Roblox account's TOTP secret (to generate a 6-digit code) and .ROBLOSECURITY (to authorize requests).
Below is a tutorial that shows how to get this TOTP as it is a bit hidden in your account settings.

### TOTP KEY TUTORIAL:
To get the key, go to Roblox privacy settings, reset/add mobile authentication.

![image](https://github.com/PogoDigitalism/RobloxTradeAuthenticator/assets/107322523/2a448f61-3781-475e-880f-ed3a7cfc95c9)

Then, click the 'Cant't scan the code? Click here for manual entry'
This is your secret key (OTP_SECRET). Copy and paste this in your code (You can share this code across multiple devices, so adding this code to your phone as well won't affect your program.
