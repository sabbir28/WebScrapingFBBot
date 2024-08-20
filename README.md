# WebScrapingFBBot

## Overview
**WebScrapingFBBot** is a Facebook bot that automates posting on Facebook using the Facebook Graph API. The bot scrapes data from websites and uses it to generate and post content automatically.

## Features
- **Automated Facebook Posting:** Posts content to Facebook using the Facebook Graph API.
- **Web Scraping:** Retrieves and processes data from websites for use in posts.
- **JSON to Database Conversion:** Converts JSON data to a database format.
- **PDF Handling:** Includes tools for managing and converting PDFs.

## File Structure
- **Core.py:** Core functionality of the bot.
- **JSONToDBConverter.py:** Handles conversion of JSON data to database format.
- **SQL_query.py:** Contains SQL queries used by the bot.
- **config.py:** Configuration file for API credentials and settings.
- **app.py:** Main application script to run the bot.
- **FB/**: Directory for Facebook-related scripts or modules.
- **PDF/**: Directory for PDF-related scripts or files.
- **notice/**: Stores runtime details that are not deleted.
- **dump/**: Directory or file for temporary storage (ignored by Git).

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/sabbir28/WebScrapingFBBot.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd WebScrapingFBBot
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Configure your settings:**
   - Update `config.py` with your Facebook Graph API credentials and other necessary settings.
2. **Run the bot:**
   ```bash
   python app.py
   ```

## Contributing
Contributions are welcome! Please open issues or submit pull requests with your improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](https://sabbir28.github.io/privacy-policy.html) file for details.

### What’s Included
- **Project Overview:** Explains what the project does.
- **Features:** Lists the key functionalities of your bot.
- **File Structure:** Describes the purpose of each file and directory.
- **Installation:** Provides steps to clone the repository and install dependencies.
- **Usage:** Instructions on how to configure and run the bot.
- **Contributing:** Information for potential contributors.
- **License:** Mentions the project license.
