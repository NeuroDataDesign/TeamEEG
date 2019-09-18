# checking for equality uses == operator and is case sensitive, can use lower()
# checking for not equal is !=
# can also do < <= > >= for math
# if statements use same rules as for loops, end with : at top then indent
# use and to for needing two conditions, sometimes parentheses help readability
# ditto for or
# keyword in to check for a value in a list, not in
age = 17
if age >= 18:
	print('You are old enough to vote!')
else:
	print('Sorry, you are too young to vote.')

if age < 4:
	price = 0
elif age < 18:
	price = 25
else:
	price = 40
print(f"Your admission cost is ${price}.")
# combining for loops and if statements
# to check if a list is empty do if nameofvariable:, true if has at least one element
available_toppings = ['mushrooms','olices','green peppers','pepperoni','pineapple']
requested_toppings = ['mushrooms','french fries','pepperoni']
for requested_topping in requested_toppings:
	if requested_topping in available_toppings:
		print(f'Adding {requested_topping}.')
	else:
		print(f"Sorry, we don't have {requested_topping}.")
print('\nFinished making your pizza!')