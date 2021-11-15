from posixpath import join
from tkinter.constants import WORD
import enchant

cipher = input("enter the cipher\n(if the result is empty, there are no meaningful words) ")
d = enchant.Dict("en_US")

for n in range(9,25):
    def break_cipher():
        list = []
        for letter in cipher:
            if(ord(letter) < (ord("a")+n)): 
                letter = chr(ord(letter)+ord("z")-ord("a")-n+1)
                list.append(letter)
            else:
                letter = chr(ord(letter)-n)
                list.append(letter)
        return list

    c = "".join(break_cipher())
    if d.check(c) is True:
        print("\n")
        print(c, end = "")
    else:
        print("", end = "")
        




