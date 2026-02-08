# CS 340 README: CRUD Python Module

Ebony Jones

## About the Project

This project is a Python module that provides CRUD (Create, Read, Update, Delete) operations for managing animal records in a MongoDB database. The module is designed to work with the Austin Animal Center (AAC) database, which contains information about animals in the shelter system. This project includes all four CRUD operations: Create, Read, Update, and Delete, providing complete database management functionality for the Austin Animal Center database.

## Motivation

The purpose of this project is to create a reusable Python module that can be integrated into larger applications, such as a web-based dashboard for the Grazioso Salvare organization. By abstracting the database operations into a dedicated class, the code becomes more maintainable, testable, and easier to understand. This modular approach also allows other developers to use the same CRUD functionality without needing to understand the underlying MongoDB connection details.

## Getting Started

To use this CRUD Python module, you will need to have the following set up:

**Database Setup:** In the Module Three milestone, I set up a MongoDB database named "aac" with a collection called "animals." The database contains animal shelter data imported from a CSV file. I also created a user account "aacuser" with readWrite permissions to securely access the database.

**User Authentication:** The module uses username and password authentication to connect to MongoDB. The credentials are stored as variables within the class and are passed to the MongoClient for secure database access.

**Module Development:** I created the AnimalShelter class with create() and read() methods. The main challenge I encountered was ensuring proper error handling and return values. I solved this by using try-except blocks and returning appropriate boolean values (True/False) for create operations and lists for read operations. This makes the module more robust and easier to debug.

## Installation

The following tools and libraries are required to use this module:

- **Python 3.x:** The programming language used to write the module. Python was chosen because it is widely used in data science and has excellent MongoDB support.

- **PyMongo:** The official MongoDB driver for Python. Install using: `pip install pymongo`. I chose PyMongo because it is the recommended library for MongoDB operations in Python and provides a straightforward API.

- **MongoDB:** The NoSQL database system. MongoDB was selected because it stores data in flexible, JSON-like documents, which is ideal for the varied animal record data.

- **Jupyter Notebook:** Used for testing the module interactively. Jupyter was chosen because it allows for step-by-step testing and immediate visualization of results.

## Usage

This section demonstrates how the CRUD Python module works and how it can be used.

## Usage

This section demonstrates how the CRUD Python module works and how it can be used.

### Code Example

The AnimalShelter class provides four main methods:

**create(data):** Inserts a new document into the animals collection. Takes a dictionary of key/value pairs and returns True if successful, False otherwise.

**read(query):** Queries documents from the animals collection. Takes a dictionary of search criteria and returns a list of matching documents.

**update(query, update_data):** Modifies existing documents in the animals collection. Takes two dictionaries: one to find the documents (query) and one with the update operations (update_data). Returns the number of documents modified.

**delete(query):** Removes documents from the animals collection. Takes a dictionary of search criteria and returns the number of documents deleted.

Example usage showing all four operations:

from CRUD_Python_Module import AnimalShelter

shelter = AnimalShelter()

# Create a new animal record
new_animal = {"name": "Test Dog", "animal_type": "Dog", "age_upon_outcome": "2 years"}
result = shelter.create(new_animal)  # Returns True

# Read animal records
dogs = shelter.read({"animal_type": "Dog"})

# Update animal records
update_result = shelter.update(
    {"name": "Test Dog"},
    {"$set": {"age_upon_outcome": "3 years"}}
)  # Returns number of records modified

# Delete animal records
delete_result = shelter.delete({"name": "Test Dog"})  # Returns number of records deleted

### Tests

I tested the module using a Jupyter Notebook (ModuleFourTestScript.ipynb). The test script performs the following:

- Creates an instance of the AnimalShelter class
- Tests the create() method by inserting a new test animal record
- Verifies the insertion by using read() to retrieve the newly created record
- Tests read() on existing data by querying for Labrador Retrievers

**Test Results:** The CREATE test returned True, confirming successful insertion. The READ test found the newly created record and also successfully retrieved 55 existing Labrador Retriever records from the database.

### Screenshots

![CRUD Python Module](crud_module.jpg)

*Figure 1: The AnimalShelter class with create() and read() methods*

![Test Results](test_results.jpg)

*Figure 2: Successful execution of the test script showing CREATE and READ operations*

<img width="2094" height="432" alt="Connection Success" src="https://github.com/user-attachments/assets/047ad913-f69b-4be7-8f05-b6fd5f7a6f6d" />

*Figure 3: Successful connection to the MongoDB database using aacuser credentials*

<img width="2306" height="587" alt="UPDATE Test" src="https://github.com/user-attachments/assets/3670811a-35d6-4547-be06-93b6d1db4e6d" />

*Figure 4: UPDATE test showing successful modification of records, changing age from "2 years" to "3 years"*

<img width="2286" height="643" alt="DELETE Test " src="https://github.com/user-attachments/assets/bd38794b-add2-4983-aaed-4dc3dd4fd667" />

*Figure 5: DELETE test showing successful removal of Test Dog records, with verification confirming 0 records remain*

## Contact

Ebony Jones
