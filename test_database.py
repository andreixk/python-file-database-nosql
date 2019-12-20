import pytest
from mc.ut.database import DBA
import os.path
import copy

first_collect_name = 'first-collection'
other_collect_name = 'other-collection'
mock_doc_first = ['a', 'b', 'c']
mock_doc_other = ['e', 'f', 'g']

class DBAMocked(DBA):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.__data = {
            first_collect_name: {
                'test': mock_doc_first
            },
            other_collect_name: {
                'test': mock_doc_other
            },
            mock_collection: { },
        }
    @property
    def _DBA__collection(self):
        return self.__data[self.collection_name]
    def _DBA__collection_exists(self):
        return self.collection_name in [other_collect_name, first_collect_name, mock_collection]
    def _DBA__collection_update(self, new_collection):
        self.__data[self.collection_name] = new_collection


@pytest.fixture
def mock_collection():
    return '/tmp/temp-collection'

@pytest.fixture
def FakeDB():
    return DBAMocked

@pytest.fixture
def dba(mock_collection):
    return DBA(mock_collection)

@pytest.fixture
def dba_nofile(FakeDB):
    return DBAMocked(mock_collection)

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

def test_db_cannot_create_collection_twice(dba, delete_after):
    dba.collection_create()
    with pytest.raises(Exception):
        dba.collection_create()

def test_db_cannot_delete_twice(dba, delete_after):
    dba.collection_create()
    dba.collection_delete()
    with pytest.raises(Exception):
        dba.collection_delete()

def test_db_cannot_delete_non_existent_collection(dba, delete_after):
    with pytest.raises(Exception):
        dba.collection_delete()

def test_db_can_autocreate_collection(delete_after, mock_collection):
    dba = DBA(mock_collection, True)
    assert dba.collection_delete() is None

def test_db_allows_multiple_calls_to_same_collection(delete_after, mock_collection):
    dba = DBA(mock_collection, True)
    dba = DBA(mock_collection, True)
    assert dba.collection_delete() is None

def test_db_cannot_create_document_without_collection(dba, delete_after):
    with pytest.raises(Exception):
        dba.document_create()

def test_db_can_create_document(dba_nofile):
    doc_id = dba_nofile.document_create()
    assert doc_id != ''
    assert dba_nofile.document_find(doc_id)

def test_db_can_create_document_with_id_and_data(dba_nofile):
    data = {
        'data': 'data',
        'id': 'abc'
    }
    doc_id = dba_nofile.document_create(data)
    assert doc_id == data['id']
    assert dba_nofile.document_find(doc_id)
    del data['id']
    assert dba_nofile.document_read(doc_id) == data

def test_db_cannot_create_document_with_id_that_exists(dba_nofile):
    data = {
        'id': 'abc'
    }
    doc_id = dba_nofile.document_create(data)
    with pytest.raises(Exception):
        doc_id = dba_nofile.document_create(data)

def test_db_cannot_create_non_object_document(dba_nofile):
    class InvalidDocClass(): 
        pass
    def invalid_doc_function(): 
        pass
    with pytest.raises(Exception):
        dba_nofile.document_create('invalid doc - string')
    with pytest.raises(Exception):
        dba_nofile.document_create(['invalid doc - array'])
    with pytest.raises(Exception):
        dba_nofile.document_create(15)
    with pytest.raises(Exception):
        dba_nofile.document_create(None)
    with pytest.raises(Exception):
        dba_nofile.document_create(InvalidDocClass())
    with pytest.raises(Exception):
        dba_nofile.document_create(invalid_doc_function)

def test_db_creating_document_does_not_change_original(dba_nofile):
    data = {
        'id': 'abc',
        'name': 'cde',
    }
    original_data = copy.deepcopy(data)
    dba_nofile.document_create(data)
    assert data == original_data

def test_db_can_check_document_existence(dba_nofile):
    doc_id = dba_nofile.document_create()
    assert dba_nofile.document_find(doc_id)

def test_db_can_read_document(dba_nofile):
    expected_data = {'a': 1}
    doc_id = dba_nofile.document_create(expected_data)
    actual_data = dba_nofile.document_read(doc_id)
    assert actual_data == expected_data

def test_db_cannot_read_non_existing_document(dba_nofile):
    with pytest.raises(Exception):
        doc = dba_nofile.document_read('non-existent id')

def test_db_can_update_document(dba_nofile):
    dba = dba_nofile
    doc_id = dba.document_create()
    doc_expected = {
        'text': 'field',
        'number': 15,
        'object': [{ 'a': 'b' }]
    }
    dba.document_update(doc_id, doc_expected)
    doc_actual = dba.document_read(doc_id)
    assert doc_expected == doc_actual

def test_db_can_delete_document(dba_nofile):
    doc_id = dba_nofile.document_create()
    dba_nofile.document_delete(doc_id)
    assert dba_nofile.document_find(doc_id) == False

def test_db_can_query_collection(dba_nofile):
    items = [
        {
            'field1': 'yes',
            'field2': 'non',
        },
        {
            'field1': 'may',
            'field2': 'non',
        },
        {
            'field1': 'may',
            'field2': 'not',
        },
    ]
    for item in items:
        item_id = dba_nofile.document_create(item)
        item['id'] = item_id
    non_existent_data = dba_nofile.query({'field1': 'value'})
    assert non_existent_data == []
    expected_single_field_result = [items[1], items[2]]
    expected_field = 'field1'
    expected_value = items[1][expected_field]
    actual_data = dba_nofile.query({expected_field: expected_value})
    assert actual_data == expected_single_field_result
    expected_multiple_fields_result = [items[1]]
    actual_data = dba_nofile.query({'field1': items[1]['field1'], 'field2': items[1]['field2']})
    assert actual_data == expected_multiple_fields_result

def test_db_can_change_collection(FakeDB):
    db = FakeDB(first_collect_name)
    assert db.document_read('test') == mock_doc_first
    db.collection_change(other_collect_name)
    assert db.document_read('test') == mock_doc_other
