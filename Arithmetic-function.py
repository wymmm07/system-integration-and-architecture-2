#Exercise 6 - Artihmetic Function

def display_num(num1, num2):
  sum = int(num1) + int(num2)
  diff = int(num1) - int(num2)
  prod = int(num1) * int(num2)
  quotient = int(num1) / int(num2)
  print ("the sum of num1 and num2 is:", sum)
  print("the difference of num1 and num2 is:", diff)
  print("the product of num1 and num2 is:", prod)
  print("the quotient of num1 and num2 is:", quotient)

num1 = input("input first number: ")
num2 = input("input second number: ")
display_num(num1, num2)
