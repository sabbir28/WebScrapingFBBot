import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirestoreHelper:
    def __init__(self, cred_file):
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(cred_file)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def set_data(self, collection_name, document_id, data):
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.set(data)
            print("Data successfully written!")
        except Exception as e:
            print(f"Error writing document: {e}")

    def get_data(self, collection_name, document_id):
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                print("No such document")
                return None
        except Exception as e:
            print(f"Error getting document: {e}")
            return None
