#exercise 3 Odd or Even 
#Create a Python programs that determines if the number is Odd or Even based on the user input

value = input("what is the number? ")
if int(value) % 2 == 0:
    print(value + " is even")
else:
    print(value + " is odd")
    
