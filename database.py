import os
import uuid
import json
import copy
class DBA():
    """Database Adaptor class
    Creates a single file "database". Database will contain a JSON object.

    Usage:
        dba = DBA(database_file_name)
    """
    def __init__(self, collection_name, autocreate=False):
        self.collection_name = collection_name
        if autocreate and not self.__collection_exists():
            self.collection_create()
    @property
    def __collection(self):
        if not self.__collection_exists():
            raise Exception('Collection does not exist')
        with open(self.collection_name, 'r') as f:
            try:
                collection = json.load(f)
            except:
                collection = {}
        return collection
    def __collection_exists(self):
        return os.path.exists(self.collection_name)
    def __collection_update(self, new_collection):
        with open(self.collection_name, 'w') as f:
            json.dump(new_collection, f)
    def collection_change(self, new_collection):
        self.collection_name = new_collection
    def collection_create(self):
        if self.__collection_exists():
            raise Exception('Collection already exists')
        with open(self.collection_name, 'w') as f:
            f.write('')
    def collection_delete(self):
        if not self.__collection_exists():
            raise Exception('Collection does not exist')
        os.unlink(self.collection_name)
    def document_create(self, doc_data={}):
        """Creates a document in a collection
        
        Returns:
            string -- document id
        """
        _data = copy.deepcopy(doc_data)
        collection = self.__collection
        unique_id = _data.pop('id', str(uuid.uuid4()))
        if unique_id in collection:
            raise Exception('Specified id already exists')
        collection[unique_id] = _data or {}
        self.__collection_update(collection)
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
        if not self.document_find(doc_id):
            raise Exception('Document does not exist')
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
    def query(self, query):
        data = self.__collection
        result = []
        for key, obj in data.items():
            if query.items() <= obj.items():
                result.append({**obj, 'id': key})
        return result
