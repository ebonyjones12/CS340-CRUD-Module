# Author: Ebony Jones
# Course: CS 340 Client/Server Development
# Enhanced for CS 499 Computer Science Capstone
# Enhancement: Removed hardcoded credentials, added environment variable support,
# and added advanced query methods beyond basic CRUD operations.

import os
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user=None, password=None, host=None, port=None, db=None, col=None):
        # Enhancement: Credentials are now pulled from environment variables instead of
        # being hardcoded in the source code. This prevents sensitive information from
        # being exposed in version control or shared code.
        # If values are passed in directly they will be used, otherwise the code
        # falls back to environment variables, and finally to safe defaults.

        USER = user or os.environ.get('MONGO_USER', 'aacuser')
        PASS = password or os.environ.get('MONGO_PASS', '')
        HOST = host or os.environ.get('MONGO_HOST', 'localhost')
        PORT = port or int(os.environ.get('MONGO_PORT', 27017))
        DB = db or os.environ.get('MONGO_DB', 'aac')
        COL = col or os.environ.get('MONGO_COL', 'animals')

        # Initialize Connection
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    # ==================== BASIC CRUD OPERATIONS ====================

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
                result = self.collection.insert_one(data)
                return result.acknowledged
            except Exception as e:
                print(f"Error during insert: {e}")
                return False
        else:
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
                cursor = self.collection.find(query)
                return list(cursor)
            except Exception as e:
                print(f"Error during read: {e}")
                return []
        else:
            return []

    # Method to implement the U (Update) in CRUD
    def update(self, query, update_data):
        """
        Updates document(s) in the animals collection.

        Args:
            query: A dictionary containing key/value pairs to find documents
            update_data: A dictionary with update operations (use $set, $inc, etc.)

        Returns:
            The number of documents modified
        """
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_many(query, update_data)
                return result.modified_count
            except Exception as e:
                print(f"Error during update: {e}")
                return 0
        else:
            return 0

    # Method to implement the D (Delete) in CRUD
    def delete(self, query):
        """
        Deletes document(s) from the animals collection.

        Args:
            query: A dictionary containing key/value pairs to find documents to delete

        Returns:
            The number of documents deleted
        """
        if query is not None:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Error during delete: {e}")
                return 0
        else:
            return 0

    # ==================== ADVANCED QUERY METHODS ====================

    def read_sorted(self, query, sort_field, sort_direction="asc", limit=0):
        """
        Enhancement: Queries documents and returns them sorted by a specified field.
        This goes beyond basic CRUD by adding sorting and limiting capabilities
        that are useful for dashboard displays and reporting.

        Args:
            query: A dictionary containing key/value lookup pairs
            sort_field: The field name to sort by (e.g. "age_upon_outcome_in_weeks")
            sort_direction: "asc" for ascending, "desc" for descending
            limit: Maximum number of results to return (0 means no limit)

        Returns:
            A sorted list of results if successful, empty list otherwise
        """
        if query is None:
            return []
        try:
            direction = ASCENDING if sort_direction.lower() == "asc" else DESCENDING
            cursor = self.collection.find(query).sort(sort_field, direction)
            if limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error during sorted read: {e}")
            return []

    def read_by_outcome_type(self, outcome_type):
        """
        Enhancement: Retrieves all animals filtered by a specific outcome type.
        Outcome types include Adoption, Transfer, Return to Owner, and Euthanasia.
        This supports dashboard filtering for animal rescue use cases.

        Args:
            outcome_type: A string representing the outcome type to filter by

        Returns:
            A list of matching animal records
        """
        if not outcome_type:
            return []
        try:
            cursor = self.collection.find({"outcome_type": outcome_type})
            return list(cursor)
        except Exception as e:
            print(f"Error during outcome type read: {e}")
            return []

    def get_breed_summary(self, animal_type=None):
        """
        Enhancement: Uses MongoDB aggregation pipeline to count animals grouped by breed.
        This is an advanced database operation that goes beyond CRUD by using
        the aggregation framework to produce summary statistics useful for reporting.

        Args:
            animal_type: Optional filter to limit results to one animal type (e.g. "Dog")

        Returns:
            A list of dictionaries with breed and count fields, sorted by count descending
        """
        try:
            match_stage = {}
            if animal_type:
                match_stage = {"$match": {"animal_type": animal_type}}
            else:
                match_stage = {"$match": {}}

            pipeline = [
                match_stage,
                {"$group": {"_id": "$breed", "count": {"$sum": 1}}},
                {"$sort": {"count": DESCENDING}},
                {"$project": {"breed": "$_id", "count": 1, "_id": 0}}
            ]
            result = list(self.collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"Error during breed summary aggregation: {e}")
            return []

    def read_by_age_range(self, min_weeks, max_weeks):
        """
        Enhancement: Retrieves animals within a specific age range in weeks.
        This uses a MongoDB range query which is more advanced than a simple
        key/value lookup and supports age-based filtering for rescue operations.

        Args:
            min_weeks: Minimum age in weeks
            max_weeks: Maximum age in weeks

        Returns:
            A list of animals within the specified age range
        """
        try:
            query = {
                "age_upon_outcome_in_weeks": {
                    "$gte": min_weeks,
                    "$lte": max_weeks
                }
            }
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as e:
            print(f"Error during age range read: {e}")
            return []
