import requests

# Replace these variables with your Facebook app details
APP_ID = '761434701600961'
REDIRECT_URI = 'sabbir28.github.io'
SCOPE = 'email,public_profile'

# Create the authorization URL
auth_url = f'https://www.facebook.com/v14.0/dialog/oauth?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}'

print('Go to the following URL to log in with Facebook:')
print(auth_url)
