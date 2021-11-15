def is_in_binary(lst, val):
    if len(lst) == 0:
        return False  
    start = 0
    end = len(lst)
    while end - start > 1:
        middle = (start +end)//2
        if val > lst[middle]:
            start = middle
        else:
            end = middle 
    return lst[start] == val   
