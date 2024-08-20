import requests

class FacebookPostDeleter:
    def __init__(self, access_token, page_id):
        self.access_token = access_token
        self.page_id = page_id
    
    def get_posts(self):
        url = f"https://graph.facebook.com/v17.0/{self.page_id}/posts"
        params = {
            'access_token': self.access_token,
            'limit': 100  # Get up to 100 posts per request
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print('Failed to retrieve posts:', response.status_code, response.text)
            return []

    def delete_post(self, post_id):
        url = f"https://graph.facebook.com/v17.0/{post_id}"
        params = {
            'access_token': self.access_token
        }
        response = requests.delete(url, params=params)
        if response.status_code == 200:
            print(f"Post {post_id} deleted successfully!")
        else:
            print(f"Failed to delete post {post_id}:", response.status_code, response.text)

    def delete_all_posts(self):
        posts = self.get_posts()
        while posts:
            for post in posts:
                post_id = post['id']
                self.delete_post(post_id)
            posts = self.get_posts()

# Example usage
if __name__ == "__main__":
    ACCESS_TOKEN = 'EAAK0hVTomMEBO0URPZBnmNOZCYZAK6vfBZBZC0M4eoHuHCA8geO452Jsm7C3muhfGL08LOByiqdEIjSbJKuOUMZA1L7gzfrtkWzu7lpXw8aXqZAWvZAXYu3dPPxfGJzmaYmgZBnYyzwE0gXdG6kS1QLY70wcvlvuBAEKieWF3HN8x3zQcbG676stU6unZC2cI4Lrm7QKIPCWqEoqmIhVNGczSka9vr'
    PAGE_ID = '394881123708990'  # Your page ID

    deleter = FacebookPostDeleter(ACCESS_TOKEN, PAGE_ID)
    deleter.delete_all_posts()
