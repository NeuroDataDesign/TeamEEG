# can't run user input from sublime, but it executes just like matlab
# modulo operator gives the remainder, its the % operator
# while loops are just like matlab again, not equal operator is !=
# using a flag is really helpful, so like setting a variable to say something is active
# break to exit a while loop, a loop starting with while True: runs to break
# continue sets the loop back to the start without doing rest of loop code
# you can increment something by going +=1
# control C to exit terminal window displaying output
unconfirmed_users = ['joe','paul','steve']
confirmed_users = []
while unconfirmed_users:
	current_user = unconfirmed_users.pop()
	print(f"Verifying user: {current_user.title()}")
	confirmed_users.append(current_user)
print('\nThe following users have been confirmed:')
for confirmed_user in confirmed_users:
	print(confirmed_user.title())
# remove all instances of something in a list
pets = ['dog','cat','rat','dog','cat','fish']
while 'cat' in pets:
	pets.remove('cat')
print(pets)