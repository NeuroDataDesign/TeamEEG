# dictionaries are like matlab structures
# written as mydict = {'key','value'}
# function get() used to check and see if a field exists
fav_numbers = {'pat':5,'jim':9,'tom':2,'john':5}
print(f"Pat's favorite number is {fav_numbers['pat']}")
for name, fav in fav_numbers.items():
	print(f"{name.title()}'s favorite number is {fav}.")

friends = ['tom','linda']
for name in fav_numbers.keys():
	print(name.title())

	if name in friends:
		number = fav_numbers[name]
		print(f"\t{name.title()}, I see you like {number}")
	else:
		print(f"\t{name.title()}, please take the survey!")

print("The following numbers are favorites:")
for number in set(fav_numbers.values()):
	print(number)
# Can do dictionaries inside lists or lists inside dictionaries
# Can also do dictionaries inside dictionaries
users = {'czurn': {'first':'claire','last':'zurn'},'lblatti':{'first':'luke','last':'blatti'}}
for username,user_info in users.items():
	print(f"\nUsername:{username}")
	full_name = f"{user_info['first']} {user_info['last']}"
	print(f"\tFull name: {full_name.title()}")
