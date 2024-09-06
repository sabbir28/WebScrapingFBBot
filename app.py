from Detabace.FirestoreHelper import FirestoreHelper

# Path to your Firebase service account key JSON file
cred_file = 'google-services.json'

# Initialize FirestoreHelper
firestore_helper = FirestoreHelper(cred_file)

# Example usage: Setting data
data = {
    'name': 'John Doe',
    'age': 30
}
firestore_helper.set_data('users', 'user1', data)

# Example usage: Getting data
document_data = firestore_helper.get_data('users', 'user1')
if document_data:
    print(f"Document data: {document_data}")
