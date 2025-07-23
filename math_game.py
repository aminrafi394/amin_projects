import random

operators = ["+", "-", "*", "/"]
k = random.randint(0, 3)
# operators[k]
a = random.randint(1, 100)
b = random.randint(1, 100)
if k == 3:
    while a % b != 0:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

# print(a, b)

c = int(input("{} {} {} = ".format(a, operators[k], b)))
if k == 0:
    if c == a + b:
        print("good")
    else:
        print("bad")

# e = int(input())
if k == 2:
    if c == a * b:
        print("correct")
    else:
        print("wrong")


# while a%2 and b%2==0 a%2 and b%2
# d = int(input())
if k == 3:
    if c == a / b:
        print("exactly")
    else:
        print("it is not exactly")

# f = int(input())
if k == 1:
    if c == a - b:
        print("answer is correct")
    else:
        print("answer is wrong")
