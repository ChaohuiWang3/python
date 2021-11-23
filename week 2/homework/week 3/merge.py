def mergesort(lst):
    #sort lst
    if len(lst) <= 1:
        return lst
    pivot = len(lst) // 2
    lst1 = mergesort(lst[:pivot])
    lst2 = mergesort(lst[pivot:])
    return merge(lst1, lst2)



def merge(lst1, lst2):
    # merge two sorted lists
    merged_list = []
    index1 = 0
    index2 = 0
    len1 = len(lst1)
    len2 = len(lst2)

    while index1 < len1 or index2 < len2:
        if index2 ==len2 or \
            (index1 < len1 and lst1[index1] < lst2[index2]):
            merged_list.append(lst1[index1])
            index1 += 1
        else:
            merged_list.append(lst2[index2])
            index2 += 1

    return merged_list


def test_mergesort():
    assert(mergesort([]) == [])
    assert(mergesort([1]) == [1])
    assert(mergesort([1,2,3,4]) == [1,2,3,4])
    assert(mergesort([1,4,3,2]) == [1,2,3,4])
    assert(mergesort([5,4,3,2,1]) == [1,2,3,4,5])


def test_sortstr():
    assert(mergesort(["abc"]) == ["abc"])
    assert(mergesort(["ba","aa", "bbbb", "a"]) == \
           ["a", "aa", "ba", "bbbb"])
