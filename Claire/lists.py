pals = ['sydney','mikala','victoria','nataly']
print(pals[0].title())#first index
print(pals[-1].title())#last index
pals.append('julia')#adds to end
print(pals[-1].title())#so now we see this changed
pals.insert(1,'hannah')#adding in new at 1, shifting after 1 right
print(pals)
knew_first = pals.pop(4)#popping out the one at idx 4
print(pals)
print(knew_first)
pals.remove('mikala')#removing by value not index
print(pals)
print(sorted(pals))#sorting alphabetically
print(len(pals))#length
# checking out for loops
for pal in pals:#important to remember the colon
	print(f'I love ya, {pal.title()}!')
print('Gotta end for loops')# no need for an end statemtent just no indent
# Now for some number lists
squares = []
for val in range(2,11,2):#allowing me to jump by 2, ends at 10
	squares.append(val**2)#square and add to list
print(squares)
squares = [val**2 for val in range(1,15)]# efficiency way
print(squares)
# some slicing of lists
print(pals[1:])#indexing second to end
print(pals[-2:])#second from last to end
newpals = pals[:]#copying, important to do the [:] otherwise the lists are tied
newpals.append('gaby')
print(pals)#showing they are different
print(newpals)
# tuples 
dimensions = (400,100)#can't change individual values, can reassign whole variable
for dimension in dimensions:
	print(dimension)