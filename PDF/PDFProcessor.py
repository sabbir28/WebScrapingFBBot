import os
import urllib.request
import random
import string
import json

class PDFProcessor:
    def __init__(self, pdf_url, destination_folder):
        self.pdf_url = pdf_url
        self.destination_folder = destination_folder
        self.folder_name = self.generate_unique_folder_name()
        self.full_folder_path = os.path.join(self.destination_folder, self.folder_name)
        os.makedirs(self.full_folder_path, exist_ok=True)
    
    def generate_unique_folder_name(self):
        # Generate a random folder name with 8 characters
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    def download_pdf(self):
        pdf_path = os.path.join(self.full_folder_path, 'document.pdf')
        try:
            urllib.request.urlretrieve(self.pdf_url, pdf_path)
            return pdf_path
        except Exception as e:
            raise Exception(f"Failed to download PDF: {e}")
    
    def create_json(self, pdf_path):
        full_pdf_path = os.path.abspath(pdf_path)
        details = {
            "folder_name": self.folder_name,
            "pdf_url": self.pdf_url,
            "pdf_file": full_pdf_path
        }
        json_path = os.path.join(self.full_folder_path, 'details.json')
        with open(json_path, 'w') as json_file:
            json.dump(details, json_file, indent=4)
    
    def process(self):
        pdf_path = self.download_pdf()
        self.create_json(pdf_path)

# Usage example:
# pdf_url = 'https://dhakaeducationboard.gov.bd/data/20240815145651126185.pdf'
# destination_folder = 'path/to/your/destination/folder'
# processor = PDFProcessor(pdf_url, destination_folder)
# processor.process()

# print(f"PDF downloaded and details saved in folder: {processor.full_folder_path}")
