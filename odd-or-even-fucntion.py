#Exercise 7: Odd_or_even_functions.py

def odd_or_even():
    value = input("what is the number? ")
    if int(value) % 2 == 0:
        print(value + " is even")
    else:
        print(value + " is odd")
odd_or_even()
