import os
import uuid
import json
class DBA():
    """Database Adaptor class
    Creates a single file "database". Database will contain a JSON object.
    
    Usage:
        dba = DBA(database_file_name)
    """
    def __init__(self, collection_name):
        self.collection_name = collection_name
    @property
    def __collection(self):
        with open(self.collection_name, 'r') as f:
            try:
                collection = json.load(f)
            except:
                collection = {}
        return collection
    def __collection_update(self, new_collection):
        with open(self.collection_name, 'w') as f:
            json.dump(new_collection, f)
    def collection_create(self):
        with open(self.collection_name, 'w') as f:
            f.write('')
    def collection_delete(self):
        if os.path.exists(self.collection_name):
            os.unlink(self.collection_name)
    def create_document(self):
        """Creates a document in a collection
        
        Returns:
            string -- document id
        """
        collection = self.__collection
        unique_id = str(uuid.uuid4())
        collection[unique_id] = {}
        with open(self.collection_name, 'w') as f:
            json.dump(collection, f)
        return unique_id
    def document_find(self, doc_id):
        """Determines whether specified document exists in collection
        
        Arguments:
            doc_id {string} -- ID of the document
        
        Returns:
            boolean -- whether the document exists
        """
        return doc_id in self.__collection
    def document_delete(self, doc_id):
        collection = self.__collection
        del collection[doc_id]
        self.__collection_update(collection)
    def document_read(self, doc_id):
        """Read a full document from collection
        
        Arguments:
            doc_id {string} -- Document ID
        
        Returns:
            object -- Full document body
        """
        return self.__collection[doc_id]
    def document_update(self, doc_id, doc_data):
        """Updates a specified document in collection
        
        Arguments:
            doc_id {string} -- ID of the document to update
            doc_data {object} -- Full body of the document
        """
        collection = self.__collection
        collection[doc_id] = doc_data
        self.__collection_update(collection)