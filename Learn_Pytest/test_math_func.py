import math_func
import pytest

import sys #inf despre python

@pytest.mark.skipif(sys.version_info < (3, 3),reason="skip")
#@pytest.mark.skip(reason="do not run number add test")
#ca sa dam skip la un test
#@pytest.mark.number
def test_add():
    assert math_func.add(7,3) == 10
    assert math_func.add(7) == 9
    print(math_func.add(7,3),'--------')
    #daca executam pytest -v -s apare printul

#@pytest.mark.number
def test_product():
    assert math_func.product(5,5) == 25
    assert math_func.product(5) == 10
#vrem sa vedem daca funct returneaza rez dorit

# daca dam pytest name -v ne da mai frum ??
#merge sa rulam si direct cu py.test fara nimic daca punem numele cu"test_"
# tot cu py.test trebuie sa punem si numele scriptului cu "test_"
#altfel merge sa rulam cu comanda clasica

#@pytest.mark.strings
def test_add_strings():
    result = math_func.add('Hello',' World')
    assert result == 'Hello World'
    assert type(result) is str
    assert 'Heldlo' not in result

#@pytest.mark.strings
def test_product_strings():
    assert math_func.product('Hello ',3) == 'Hello Hello Hello '
    result = math_func.product('Hello ')
    assert result =='Hello Hello '
    assert type(result) is str
    assert 'Hello' in result

#pytest test_math_func.py::test_add pentru a rula doar o funct
#pytest -v -k "add" pentru a rula doar funct care contin "add" la nume
#pytest -v -k "add or string" aici care contin si "add" si "string"
#pytest -v -k "add and string" merge si asa

#dupa decoratori
#pytest -v -m strings

#ptyest cu -v -x (dupa ce pica un test se opreste)
#ptyest cu -v -x --tb=no (ne arata mai putin)
#ptyest cu -v --maxfail=2 (daca pica mai mult de 2 teste se opreste)
