import json
import os
from datetime import datetime
import sqlite3
from Core import ExamNotice
from JSONToDBConverter import JSONToDBConverter
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from PDF.PDFProcessor import PDFProcessor
from PDF.PDFConverter import PDFConverter
from FB.FacebookPoster import FacebookPoster
from config import PAGE_ACCESS_TOKEN,PAGE_ID


def load_json_data(file_path):
    """
    Load JSON data from a file and return the folder name, PDF URL, and PDF file path.
    
    Args:
    - file_path (str): The path to the JSON file.
    
    Returns:
    - tuple: A tuple containing the folder name, PDF URL, and PDF file path.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        folder_name = data.get("folder_name")
        pdf_url = data.get("pdf_url")
        pdf_file = data.get("pdf_file")
        
        return folder_name, pdf_url, pdf_file
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
    except KeyError as e:
        print(f"Error: Missing expected key {e} in the JSON file.")

def format_notification_details(id, title, last_updated, download_link):
    # Initialize date_obj to None to handle error case
    date_obj = None
    
    try:
        # Parse date assuming the format is 'dd/mm/yyyy'
        date_obj = datetime.strptime(last_updated, '%d/%m/%Y')
        formatted_date = date_obj.strftime('%d/%m/%Y')
    except ValueError:
        formatted_date = last_updated  # Fallback if the date format is incorrect
    
    # Check if date_obj was successfully created
    if date_obj:
        # Generate dynamic tags based on the date
        year = date_obj.year
        month = date_obj.strftime('%m')
        
        # Example tags based on year and month
        tags = [
            f"#HSC{year}",
            f"#SABBIR28",
            f"#HSC{str(year)[-2:]}",  # Tag with last 2 digits of year (e.g., #HSC16)
            f"#HSC"
        ]
    else:
        # Default tags if date_obj could not be created
        tags = [
            f"#NoDateTag",
            f"#SABBIR28"
        ]
    
    # Combine tags into a single string
    tags_string = " ".join(tags)
    
    details = (
        f"{title}:\n"
        f"Date: {formatted_date}\n"
        f"Download Link: {download_link}\n"
        f"\n"
        f"\n"
        f"ID: {id}\n"
        f"\n"
        f"\n"
        f"{tags_string}\n"
    )
    return details


class ExamNoticeManager:
    def __init__(self, fetch_url, json_path, db_file):
        self.fetch_url = fetch_url
        self.json_path = json_path
        self.db_file = db_file

    def fetch_exam_notices(self):
        """Fetches exam notices from the URL and saves them to a JSON file."""
        try:
            response = requests.get(self.fetch_url)
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
                        notices.append(notice.to_dict())
                    except (AttributeError, TypeError, IndexError) as e:
                        print(f"Error processing row: {e}")
                        continue
        else:
            print("No table found on the webpage.")
        
        self.save_to_json(notices)

    def save_to_json(self, notices):
        """Saves the exam notices to a JSON file."""
        try:
            # Convert to absolute path
            json_path = os.path.abspath(self.json_path)
            directory = os.path.dirname(json_path)

            # Ensure the directory exists
            if directory and not os.path.exists(directory):
                print(f"Directory '{directory}' does not exist. Creating...")
                os.makedirs(directory)

            # Save to JSON file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(notices, f, ensure_ascii=False, indent=4)
            
            print(f"Saved {len(notices)} notices to the JSON file at {json_path}")
        except OSError as e:
            print(f"Error saving to JSON file: {e}")

    def convert_and_save(self):
        """Converts the JSON file to an SQLite database."""
        converter = JSONToDBConverter(self.json_path, self.db_file)
        converter.convert_and_save()


class Facebook:
    def __init__(self, db_path):
        """
        Initialize the Facebook class with the path to the .db file.

        :param db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        # ading tracking manejer for my project
        self.db_manager = TraceManager('example.db')
        
        self.fb_poster = FacebookPoster(PAGE_ID, PAGE_ACCESS_TOKEN)

    def get_last_id(self):
        """
        Get the last ID from the notifications table.

        :return: The last ID as an integer
        """
        self.cursor.execute("SELECT MAX(id) FROM notifications")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def get_notifications(self):
        """
        Retrieve all notifications from the database in descending order by ID.

        :return: A list of tuples representing the notifications
        """
        self.cursor.execute("SELECT * FROM notifications ORDER BY id DESC")
        return self.cursor.fetchall()

    def print_notifications(self):
        """
        Print all notifications from the database, from the most recent to the oldest.
        """
        notifications = self.get_notifications()
        for notification in notifications:
            id, title, last_updated, download_link = notification
            
            # there is a way or process for uplaod those file onw by one
            
            if self.db_manager.record_exists(url=download_link):
                pass # alrady exist that entry or poted
            else:
                # adding that deta into traking system
                self.db_manager.add_record(download_link) 
                processor = PDFProcessor(pdf_url=download_link,destination_folder="dump")
                processor.process()
            
                # Construct the path to the JSON file
                self.tmp_d = os.path.join("dump", processor.folder_name, "details.json")

                # Print the path for verification
                print(f"Path to the details JSON file: {self.tmp_d}")
                
                folder_name, pdf_url, pdf_file = load_json_data(self.tmp_d)
                
                converter = PDFConverter(pdf_file, os.path.join("dump", processor.folder_name, "image"))
                converter.convert_pdf_to_images()
                
                print(converter.get_image_paths())
                #self.fb_poster.post_image_with_text(image_path=converter.get_image_paths()[0],message=title)
            
                formatted_details = format_notification_details(id, title, last_updated, download_link)
                
                # Check if there's more than one image
                include_post_number = len(converter.get_image_paths()) > 1

                for index, image_path in enumerate(converter.get_image_paths(), start=1):
                    if include_post_number:
                        message = f"Post Number: {index}\n{formatted_details}"
                    else:
                        message = formatted_details
                    
                    self.fb_poster.post_image_with_text(image_path=image_path, message=message)
            
                print(f"ID: {id}")
                print(f"Title: {title}")
                print(f"Last Updated: {last_updated}")
                print(f"Download Link: {download_link}")
                print("-" * 40)

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()

class TraceManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self._create_table()

    def _create_table(self):
        """Creates the table if it doesn't exist."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    date TEXT
                )
            ''')
            conn.commit()

    def add_record(self, url):
        """Adds a new record to the database with the current date and time."""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO records (url, date)
                    VALUES (?, ?)
                ''', (url, current_date))
                conn.commit()
                print(f"Record with URL '{url}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"Record with URL '{url}' already exists.")

    def record_exists(self, url):
        """Checks if a record with the given URL exists."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM records WHERE url = ?
            ''', (url,))
            result = cursor.fetchone()
            return result is not None

    def display_all_records(self):
        """Displays all records in the database."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records')
            rows = cursor.fetchall()
            for row in rows:
                print(row)


# Usage example
if __name__ == "__main__":
    fetch_url = 'https://dhakaeducationboard.gov.bd/index.php/site/product/hsccorner'
    json_path = 'notice/notices.json'
    db_file = 'notice/data.db'
    
    manager = ExamNoticeManager(fetch_url, json_path, db_file)
    manager.fetch_exam_notices()
    manager.convert_and_save()
    
    #complite initlize now time for upload that on facebook
    
    fb = Facebook(db_file)
    print(f"Last ID: {fb.get_last_id()}")
    fb.print_notifications()
    fb.close()
