# Flat-file tiny NoSQL "database"

This is not strictly speaking a database, but a small abstraction wrapper for working with a local file as a nosql "database".

Usage:

To set up database:

```Python
from .database import DBA
dba = DBA('/tmp/my-db.json')
dba.collection_create() # creates the database file
```

You can also specify to create it automatically:
```Python
from .database import DBA
dba = DBA('/tmp/my-db.json', autocreate=True)
```

To switch to a different collection:
```Python
from .database import DBA
dba = DBA('/tmp/my-db.json')
dba.collection_change('/tmp/other-db.json')
```

**NB:** after switching the collection, you need to call `dba.collection_create()` if it does not exist yet

Working with documents:
```Python
doc_id = dba.create_document() # creates a new document in the collection and returns its ID

dba.document_update(doc_id, {'a':'b', 'c': 'd'}) # will save the object into the document

obj = dba.document_read(doc_id) # will return {'a': 'b', 'c': 'd'}

dba.create_document({'v':'w', 'x': 'y'}) # you can create document with appropriate data directly

# now that you have two documents, you can search the database
dba.query({'a':'b'}) # will return [{'a':'b', 'c': 'd', 'id': '2h93f917'}], where 'id' is the id of the document

dba.document_delete(doc_id) # deletes the document

dba.collection_delete() # deletes the database file
```

To run tests:
```bash
pytest
```
