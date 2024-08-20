import requests

class FacebookPoster:
    def __init__(self, page_id, access_token):
        self.page_id = page_id
        self.access_token = access_token
    
    def post_to_facebook(self, message):
        url = f'https://graph.facebook.com/{self.page_id}/feed'
        
        payload = {
            'message': message,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print('Post was successful!')
            print(response.json())
        else:
            print('Failed to post:', response.status_code, response.text)

    def post_image_with_text(self, image_path, message):
        url = f'https://graph.facebook.com/{self.page_id}/photos'
        
        payload = {
            'message': message,
            'access_token': self.access_token
        }
        
        files = {
            'source': open(image_path, 'rb')
        }
        
        response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            print('Image post with text was successful!')
            print(response.json())
        else:
            print('Failed to post image with text:', response.status_code, response.text)
