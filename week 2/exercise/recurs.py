def is_in_bianry(lst, val):
    if len(lst) == 0:
        return False
    return is_in_recurs(lst, val, 0, len(lst))

def is_in_recurs(lst, val, start, end):
    if end - start == 1:
        return lst[start] == val  

    
    middle = (start +end)//2
    if val >  lst[middle]:
        return is_in_recurs(lst, val, middle, end)
    else:
        return is_in_recurs(lst, val, start, middle) 


