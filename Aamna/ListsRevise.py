
# understanding lists and ranges
# creating a list
fruits = ['apple', 'banana', 'orange']
# appending new items to the list
fruits.append("mango")
# concatenating two lists
rating = [4, 3, 2, 1]
new_fruits = fruits + rating
print(new_fruits)
print("*"*50)
# using 'is'
r = rating
if r is rating:
    print("They are both pointing to the same lists")
r = sorted(rating, reverse=True)
if r == rating:
    print("The contents are the same but they are not the same lists")
    print(r)
print("*"*50)
# creating new lists
a = list(rating)
# if you do a=rating then a will also point to the same memory location as rating
if a is rating:
    print("They are the same lists")
else:
    if a == rating:
        print("They have the same contents but are different lists")
print("*"*50)
# lists within lists
even = [2, 4, 6, 8]
odd = [1, 3, 5, 7]
numbers = [even, odd]
for n in numbers:
    print(n)
    for val in n:
        print(val)
print("*"*50)
# challenge
# print ingredients of the items in menu which do not have spam
menu = []  # another way of creating a list
menu.append(["egg", "spam", "bacon"])
menu.append(["egg", "sauage", "bacon"])
menu.append(["egg", "spam"])
menu.append(["egg", "bacon", "spam"])
menu.append(["egg", "bacon", "sausage", "spam"])
menu.append(["spam", "bacon", "sausage", "spam"])
menu.append(["spam", "egg", "spam", "spam", "bacon", "spam"])
menu.append(["spam", "egg", "sausage", "spam"])
for items in menu:
    if not "spam" in items:
        print(items)
        for ingredients in items:
            print(ingredients)
print("*"*50)
# understanding iterators-how the for loop works
num = [1, 2, 3, 4, 5, 6]
iterable = iter(num)
for n in range(0, len(num)):
    print(next(iterable))
print("*"*50)
# understanding ranges
p = range(0, 20, 3)
print(p);
o = p[::4]
print(o)
for i in o:
    print(i)
print("*"*50)

