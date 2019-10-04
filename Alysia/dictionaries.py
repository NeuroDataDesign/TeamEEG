age = {"alice" : 33, "max" : 25, "jack" : 43 } #create dictionary
print (age)
age["dan"] = 32 #add Dan to dictionary
print(age)
print(age.keys()) #print keys
print(age.values()) #print values
age.pop("jack") #delete values
age["alice"] = 13 #change value in dictionary
print(age)
print(len(age)) #length
if "alice" in age:
    print(True)
else:
    print(False) #check if key present
print("jack" in age)
age2 = age.copy() #copy dictionary
print(age2)
print (age.get("max")) #get values of max

car = { "colour" : {"red": 3, "blue" : 4}, "brand" : {"BMW" : 6, "Ford" : 8}}
print(car)
print(car["colour"]) #access nested dictionaries