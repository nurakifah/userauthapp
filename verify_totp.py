import pyotp

# Replace with the same secret you used earlier
mfa_secret = "FZZIJRESENOCPOAQ7VWYA34M4KGTMVKK"
totp = pyotp.TOTP(mfa_secret)

# Ask the user to input the TOTP code
code = input("Enter the TOTP code: ")

# Verify the code
if totp.verify(code):
    print("TOTP verification successful!")
else:
    print("Invalid TOTP code.")
