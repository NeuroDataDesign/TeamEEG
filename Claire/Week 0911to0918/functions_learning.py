# functions work the same as in matlab
# def func_name(inputs):
# positional argument is where the order you type in inputs determines what they are
# keyword arguments, you can say exactly which argument is which
# function(input1 = 'x', input2 = 'y')
# can define default values for when a parameter is not provided
# def function(input1,input2 = "default2")
# always put defaults after any non default inputs because it becomes positional
# return is how you give outputs
# making an argument optional, set its default to an empty value and ignore unless it has a value
# using this to build dictionaries is nice
def print_models(unprinted_designs,completed_models):
	"""
	Simulate printing design until none left, move to completed_models
	"""
	while unprinted_designs:
		current_design = unprinted_designs.pop()
		print(f"Printing model: {current_design}")
		completed_models.append(current_design)

def show_completed_models(completed_models):
	""" Show all the models that were printed"""
	print("\nThe following models were printed:")
	for completed_model in completed_models:
		print(completed_model)
unprinted_designs = ['phone case','pendant','keychain']
completed_models = []
print_models(unprinted_designs,completed_models)
show_completed_models(completed_models)
# to keep a copy of a list, pass it into a function as a copy[:]
# to pass in an arbitrary number of arguments, function(*input)
# similarly, put any required things first, before this, like defaults
# **args to tell python to create an empty dictionary for the name value pairs

# storing functions in modules
#define functions in a module and save it say named pizza.py
# when you want to call functions from pizza, go "import pizza"
# then accessible by pizza.functionname()
# could also do "from module_name import function_name1,functionname2"
# once imported you can call as its normal name
# can give it a different name/alias ie "from module_name import function_name as fn"
# can also import module_name as mn
# or you can import all functions in a module with "from module_name import *"
# import anything you need at the top
