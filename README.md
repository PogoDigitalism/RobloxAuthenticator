# Roblox Trade Authenticator

## This wrapper currently only provides ACCEPTING trades, additional features will be added in the future.
This is a simple wrapper written for Python to combat Roblox' new **2FA MOBILE authentication** system. Contains both a synchronous and asynchronous class with methods.

You need:
 - Roblox trade ID (will probably be a dynamic variable in your code)
 - Roblox user ID (constant/variable)
 - ROBLOSECURITY cookie (for authorization)
 - Secret Key for TOTP (tutorial on how to get that inside the code)

TradeAuthenticator.py contains the source.

This function requires the external pyotp, requests and aiohttp libraries to function. 

**To contact me:**
PogoDigitalism on Discord
