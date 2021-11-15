for a in range(1,101):
    if a%3 != 0 and a%5 != 0:
        print(a)
    if a%3 == 0 and a%5 != 0:
        print("Fizz")
    if a%3 != 0 and a%5 == 0:
        print("Buzz")
    if a%3 == 0 and a%5 == 0:
        print("FizzBuzz")