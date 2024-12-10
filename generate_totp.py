import pyotp

# Replace with your actual secret
mfa_secret = "FZZIJRESENOCPOAQ7VWYA34M4KGTMVKK"
totp = pyotp.TOTP(mfa_secret)
print("Your TOTP code is:", totp.now())