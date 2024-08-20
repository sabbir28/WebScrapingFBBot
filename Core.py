import os
import requests
from bs4 import BeautifulSoup
import json
import click

# Define the ExamNotice class
class ExamNotice:
    def __init__(self, title, last_updated, download_link):
        self.title = title
        self.last_updated = last_updated
        self.download_link = download_link

    def to_dict(self):
        return {
            "title": self.title,
            "last_updated": self.last_updated,
            "download_link": self.download_link
        }

    def __str__(self):
        return f"Title: {self.title}\nLast Updated: {self.last_updated}\nDownload Link: {self.download_link}\n"

# Function to fetch exam notices from the provided URL
def fetch_exam_notices(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'example2'})
    notices = []

    if table:
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 3:
                try:
                    title = cols[0].text.strip()
                    last_updated = cols[1].text.strip()
                    download_link = cols[2].find('a')['href']
                    if not download_link.startswith('http'):
                        download_link = f"https://dhakaeducationboard.gov.bd{download_link}"
                    notice = ExamNotice(title, last_updated, download_link)
                    notices.append(notice)
                except (AttributeError, TypeError, IndexError) as e:
                    print(f"Error processing row: {e}")
                    continue
    else:
        print("No table found on the webpage.")

    return notices

# Function to save the extracted notices into a JSON file
def save_to_json(notices, json_path):
    try:
        # Convert to absolute path
        json_path = os.path.abspath(json_path)
        directory = os.path.dirname(json_path)

        # Ensure the directory exists
        if directory and not os.path.exists(directory):
            print(f"Directory '{directory}' does not exist. Creating...")
            os.makedirs(directory)

        # Convert notices to a list of dictionaries
        notices_data = [notice.to_dict() for notice in notices]

        # Save to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(notices_data, f, ensure_ascii=False, indent=4)
        
        print(f"Saved {len(notices)} notices to the JSON file at {json_path}")
    except OSError as e:
        print(f"Error saving to JSON file: {e}")

# CLI interface
@click.command()
@click.option('--url', default='https://dhakaeducationboard.gov.bd/index.php/site/product/hsccorner', help='URL of the Dhaka Education Board HSC Corner.')
@click.option('--json_path', default='notice/notices.json', help='Path to the JSON file.')
def main(url, json_path):
    notices = fetch_exam_notices(url)
    if notices:
        save_to_json(notices, json_path)
    else:
        print("No notices were fetched.")

if __name__ == '__main__':
    main()
