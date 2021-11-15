def test_is_in():
    assert is_in([1,2,3], 1)
    assert is_in([1,2,3], 3)
    assert not is_in([1,2,3], 4)
    assert not is_in([],4)
    

def is_in(lst, target):
    for item in lst:
        if item == target:
            return True
    return False