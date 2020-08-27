#Coded by Andreas Karageorgos

from random import randint
from string import ascii_letters,digits

passwd = ""
IV = ""

chars = list(ascii_letters+digits+"~`!@#$%^&*()_+-={}[]\\:;'\"<>,./?")

l = len(chars)-1

#mixing chars
for _ in range(randint(50,100)):
    n1 = randint(0,l)
    n2 = randint(0,l)
    chars[n1], chars[n2] = chars[n2], chars[n1]

#creating passwd

passwd = "".join([chars[randint(0,l)] for _ in range(randint(100,256))])

#creating IV

IV = "".join([chars[randint(0,l)] for _ in range(16)])

print("Password and IV have ben generated !!!\n")
ans = input("Do you want to replace the key files ? [y/n]: ")
while ans != "y" and ans!="n":
    ans = input("Do you want to replace or create the files ? [y/n]: ")

if ans == "y":
    with open("key/AES.key", "w") as f:
        f.write(passwd)
        f.close()
    with open("key/IV.key", "w") as f:
        f.write(IV)
        f.close()

    print("Done !")


