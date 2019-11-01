# understanding dictionaries-unordered, access by key
fruits={"Apple":"Red, round ,and crunchy", "Pear":"Juicy and odd-shaped", "Grape":"Green, round, juicy", "Banana": "Yellow and a good source of potassium"}
# appending new elements to the fruit dictionary
fruits["Mango"]="Yellow, juicy and yummy"
print(fruits)
# printing the description associated with a key of a dictionary
print(fruits["Mango"])
# deleting an element of a dictionary
del fruits["Apple"]
print(fruits) # to delete the entire dictionary use fruit.clear()
# iterating through the dictionary and printing the description
for key in fruits:
    print(fruits.get(key)) # or print(fruits[key])
# to test if a given key exists in a dictionary
y=input("Enter the key to be searched")
print(fruits.get(y, "The key does not exist"))
# sorting the elements in a dictionary using the sort() method
ordered_keys=list(fruits.keys())
ordered_keys.sort()
for i in ordered_keys:
    print(fruits[i])
print(ordered_keys)
# making tuples from dictionaries
tup=tuple(fruits); # similarly, dictionaries can be created from tuples using the function dict()
for f in tup:
    print(f+ " - "+fruits[f]);

# creating a set-unordered, no duplicates, no access by a key unlike dictionaries, immutable
animals={"dogs", "cats", "sheep"}; # another way of creating sets are animals=set(["dogs", "cats", "sheep"])
# for accessing set elements using for loop
for a in animals:
    print(a)
# to add new animals to the set
animals.add("horse")
# performing unions between two sets
even={2,4,6,8}
odd={1,3,5,7}
print(even.union(odd)) #for intersection use even.intersection(odd)
# removing elements from set
even.discard(2)
print(even)
# finding symmetric difference
a={3,5,6,7}
print(even.symmetric_difference(a))


