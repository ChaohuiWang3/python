list = []
days = ["mon","tues","weds","thurs","fri"]
print(days)
print(len(days))
day2 = days[1]
print(day2)
days.append("sat")
days.append("sun")
print(days)
del days[0]
print(days)
days.insert(0,"mon")
print(days)
days[4]="Friday"
print(days)
days.pop(0)
print(days)
