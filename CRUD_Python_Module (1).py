# Example Python Code to Insert a Document
from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to access the MongoDB
        # databases and collections. This is hard-wired to use the aac
        # database, the animals collection, and the aac user.
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    # Method to implement the C (Create) in CRUD
    def create(self, data):
        """
        Inserts a document into the animals collection.
        
        Args:
            data: A dictionary containing key/value pairs for the document
            
        Returns:
            True if insert is successful, False otherwise
        """
        if data is not None:
            try:
                # Insert the document and check if successful
                result = self.collection.insert_one(data)
                # Return True if acknowledged
                return result.acknowledged
            except Exception as e:
                print(f"Error during insert: {e}")
                return False
        else:
            # Return False if data is empty/None
            return False

    # Method to implement the R (Read) in CRUD
    def read(self, query):
        """
        Queries for documents from the animals collection.
        
        Args:
            query: A dictionary containing key/value lookup pairs
            
        Returns:
            A list of results if successful, empty list otherwise
        """
        if query is not None:
            try:
                # Use find() to get cursor, convert to list
                cursor = self.collection.find(query)
                return list(cursor)
            except Exception as e:
                print(f"Error during read: {e}")
                return []
        else:
            # Return empty list if query is None
            return []