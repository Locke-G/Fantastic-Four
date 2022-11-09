
#Exercise 1
name = input()
print("Hello", name, "! Nice to meet you!)
print("Welcome to the Python course!")





#Exercise 2 with loop
word = input()
i=len(word)-1
reverse =""
while i >= 0:
    reverse += word[i]
    i-=1
print(reverse)




#Exercise 2 with array indices
word = input()
print(word[::-1])




#Exercise 3
number = int(input())
i = 1
j = 1
nextnumber = 0
list = [i,j]
while nextnumber < number:
    nextnumber = i+j
    if nextnumber > number:
        break
    list.append(nextnumber)
    i = j
    j = nextnumber
print(list)




# Exercise 4
number = int(input())
list = []
for i in range (0,number):
    if (i%3) != 0:
        list.append(i)
    else:
        continue
print(list)




# Exercise 5
a, b, c = int(input("a:")), int(input("b:")),int(input("c:"))
correct = False
while correct != True:
    if (a>b+c) or (b>a+c) or (c>a+b):
        print("Invalid input")
        a, b, c = int(input("a:")), int(input("b:")),int(input("c:"))
    else:
        correct = True

eq = False
iso = False
sca = False
    
if a == b and b == c:
    eq = True
if (a == b) or (a == c) or (b ==c):
    iso = True
if a != b and b != c and a != c:
    sca = True

if eq == True:
    print("eq")
if iso == True:
    print("is")
if sca == True:
    print ("sca")
if eq == False and iso == False and sca == False:
    print ("Nothing")




#Exercise 6.1
decimal = int(input())
octal = oct(decimal)
print(octal[2:])


#Exercise 6.2 (funktioniert nicht)
num = float(input())
whole, dec = repr(num).split(".")
whole = int(whole)
dec = repr(dec)
print(dec)

oct1 = oct(whole)
oct2 = ''
for x in range (1,len(dec)-1):
    a = dec[x]
    print(a)
    part = int(a)
    oct2 += repr(oct(part))

print(oct1)
print(oct2) 


