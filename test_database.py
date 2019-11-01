import pytest
from .database import DBA
import os.path

@pytest.fixture
def mock_collection():
    return '/tmp/temp-collection'

@pytest.fixture
def dba(mock_collection):
    return DBA(mock_collection)

@pytest.fixture
def delete_after(mock_collection):
    yield
    if os.path.exists(mock_collection):
        os.unlink(mock_collection)

@pytest.fixture
def setup_cleanup_collection(dba):
    dba.collection_create()
    yield
    dba.collection_delete()

def test_db_can_create_collection(dba, delete_after, mock_collection):
    dba.collection_create()
    assert os.path.exists(mock_collection)

def test_db_can_delete_collection(dba, delete_after, mock_collection):
    dba.collection_create()
    dba.collection_delete()
    assert os.path.exists(mock_collection) == False

def test_db_can_create_document(dba, setup_cleanup_collection, mock_collection):
    doc_id = dba.create_document()
    assert doc_id != ''
    assert dba.document_find(doc_id)

def test_db_can_read_document(dba, setup_cleanup_collection):
    doc_id = dba.create_document()
    doc = dba.document_read(doc_id)
    assert doc == {}

def test_db_can_update_document(dba, setup_cleanup_collection):
    doc_id = dba.create_document()
    doc_expected = {
        'text': 'field',
        'number': 15,
        'object': [{ 'a': 'b' }]
    }
    dba.document_update(doc_id, doc_expected)
    doc_actual = dba.document_read(doc_id)
    assert doc_expected == doc_actual

def test_db_can_delete_document(dba, setup_cleanup_collection):
    doc_id = dba.create_document()
    dba.document_delete(doc_id)
    assert dba.document_find(doc_id) == False
