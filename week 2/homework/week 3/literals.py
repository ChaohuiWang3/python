tw0_line_string = "Line1\nLine2"
print(tw0_line_string)

namestr = "my name is {name}".format(name = "Mark")
print(namestr)

numstr = "Dec:{num: d} | Hex:{num: x} | Oct:{num: o}".format(num=14)
print(numstr)

template = "Float:{num: .2e} Fixed:{num: .2f} Perc:{num: .2%}"
realstr = template.format(num = 0.12345)
print(realstr)