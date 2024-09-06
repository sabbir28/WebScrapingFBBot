import requests

class GoogleGenerativeLanguageAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    
    def generate_content(self, text):
        url = f'{self.base_url}?key={self.api_key}'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # Extract the generated content
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return generated_text
        else:
            response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    api_key = 'AIzaSyA7g4O4ih1EYYDP5yeRK98zV6wlfbrNdQg'  # Replace with your actual API key
    api = GoogleGenerativeLanguageAPI(api_key)
    
    try:
        result = api.generate_content("")
        print("Generated Content:")
        print(result)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

