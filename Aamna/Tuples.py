# understanding Tuples
artists=("Shawn Mendes", "Justin Bieber", "Miley Cyrus", "Chris Brown", "Lana Del Ray")
print(artists)
# artists.append("Nick Jonas") this gives an error because the tuple object is considered immutable.
artists=("Shawn Mendes", "Justin Bieber", "Miley Cyrus", "Chris Brown", "Lana Del Ray", "Nick Jonas")  # this works
# because we created a new tuple and assigned it to the same variable
print(artists)
print('*'*50)
# creating tuples within tuples
song_info = ("Side to side", "Ariana Grande"), ("Cold water", "Justin Bieber"), ("Sucker for you", "Nick Jonas"), ("Cool", "Lana Del Ray")
print(len(song_info))
print('*'*50)
# printing elements in tuples with indentation
imelda = "More Mayhem", "Imelda May", 2011, ((1, "Pulling the Rug"), (2, "Psycho"), (3, "Mayhem"), (4, "Kentish Town Waltz"))
for i in range(0, len(imelda)):
    if i<len(imelda)-1:
        print(imelda[i])
    else:
        for songs in imelda[len(imelda)-1]:
            tracknum, song = songs
            print("\t{}".format(song))
print("*"*50)
# lists in tuples
imelda = "More Mayhem", "Imelda May", 2011, [(1, "Pulling the Rug"), (2, "Psycho"), (3, "Mayhem"), (4, "Kentish Town Waltz")]
imelda[3]. append((5, "hello bean"))
print(imelda)
print("*"*50)





