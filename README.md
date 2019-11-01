# Flat-file NoSQL "database"

This is not strictly speaking a database, but a small abstraction wrapper for working with a local file as a nosql "database".

Usage:
```Python
from .database import DBA
dba = DBA('/tmp/my-db.json')
dba.collection_create() # creates the database file

doc_id = dba.create_document() # creates a new document in the collection and returns its ID

dba.document_update(doc_id, {'a':'b'}) # will save the object into the proper document

obj = dba.document_read(doc_id) # will return {'a': 'b'}

dba.document_delete(doc_id) # deletes the document

dba.collection_delete() # deletes the database file
```

To run tests:
```bash
pytest
```
