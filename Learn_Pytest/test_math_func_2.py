from math_func_2 import StudentDB

import pytest

@pytest.fixture(scope='module')# pentru a apela acest db doar o singura data
def db():
    print('-------setup--------')
    db = StudentDB()
    db.connect('data.json')
    yield db # yield e folosita ca sa dam return si totusi sa mai execute si liniile de mai jos
    print('-------teardown--------')
    db.close()
#deci aici avem un fixture si ce ne returneaza va fi dat ca si param in funct de mai jos
#SAU


# db = None
# def setup_module(module):
#     global db # global pentru a o putea folosi in celelalte functii
#     print('-------setup--------')
#     db = StudentDB()
#     db.connect('data.json')

# #eliberam resursele aici
# def teardown_module(module):
#     print('-------teardown--------')
#     db.close()

def test_scott_data(db):
    scott_data = db.get_data('Scott')
    assert scott_data['id'] == 1
    assert scott_data['name'] == 'Scott'
    assert scott_data['result'] == 'pass'

def test_mark_data(db):
    scott_data = db.get_data('Mark')
    assert scott_data['id'] == 2
    assert scott_data['name'] == 'Mark'
    assert scott_data['result'] == 'fail'