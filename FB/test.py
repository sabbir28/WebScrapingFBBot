import requests

def get_user_details(user_token):
    # URL to fetch user details
    url = 'https://graph.facebook.com/me'
    params = {
        'access_token': user_token,
        'fields': 'id,name,email,picture'
    }

    try:
        # Make the request to the Graph API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        user_info = response.json()
        user_id = user_info.get('id')
        user_name = user_info.get('name')
        user_email = user_info.get('email')
        profile_picture = user_info.get('picture', {}).get('data', {}).get('url')

        return {
            'id': user_id,
            'name': user_name,
            'email': user_email,
            'profile_picture': profile_picture
        }

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Example usage
USER_TOKEN = 'EAAK0hVTomMEBO2eGZBwrMM6LUl11d1NmmNnZCWHQgkcnq2FeW7yjWrtkQRdAS0foKvxnl7aB2IJE05MuqiMb3VBZAvTVt4zAqDlplMkDZCgdRUjdtdWwNqN2kTgACDZCG7QbaeCTSCCSErX3t9VyLxTNv98rjFedeyJ9eYS7g9m6UDnwigzc91X8mpAZDZD'
user_details = get_user_details(USER_TOKEN)
print('User Details:', user_details)
