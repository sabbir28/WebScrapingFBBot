import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# List of URLs to delete from the 'records' table
urls_to_delete = [
    'https://dhakaeducationboard.gov.bd/data/20160208103704517689.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160301105028529435.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160310115137539718.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160306125120542499.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160308121031330837.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160308123304699191.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160322164220647446.pdf',
    'https://dhakaeducationboard.gov.bd/data/20160322164808265939.pdf'
]

# Create a query string with placeholders for each URL
query = "DELETE FROM 'records' WHERE url IN ({})".format(','.join('?' * len(urls_to_delete)))

# Execute the DELETE query
cursor.execute(query, urls_to_delete)

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Specified records deleted successfully.")