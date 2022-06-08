import math_func_1
import pytest

@pytest.mark.parametrize('x, y, result',
                        [
                            (7, 3, 10),# x =7, y=3, result =10
                            ('Hello',' World','Hello World'),
                            (7.3, 2.1, 9.4)
                        ]
                        )
def test_add(x, y, result): #numele ca si mai sus la parameterize
    assert math_func_1.add(x, y) == result
    #lista va fi iterata in linia de cod de mai sus