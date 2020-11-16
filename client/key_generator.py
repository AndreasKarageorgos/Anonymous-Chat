from random import randint
from getpass import getpass
from hashlib import sha1
from sys import maxunicode
from data.libraries.AES_cryptography import encryptor

sl = "/"

passwd = ""

chars = []


while len(chars)<8:
    try:
        temp = chr(randint(0,maxunicode))
        if len(temp.encode())==4:
            chars.append(temp)
    except:
        pass

l = len(chars)-1

#mixing chars
for _ in range(randint(50,100)):
    n1 = randint(0,l)
    n2 = randint(0,l)
    chars[n1], chars[n2] = chars[n2], chars[n1]


#creating passwd

name = input("Name: ").strip()
while name=="":
    name = input("Name: ").strip()


passwd = "".join(chars)



password1 = getpass("Set up a password: ")
while password1=="":
    password1 = getpass("Set up a password: ")
password2 = getpass("Repeat password: ")

while password1!=password2:
    print("Passwords do not match.")
    password1 = getpass("Set up a password: ")
    while password1=="":
        password1 = getpass("Set up a password: ")
    password2 = getpass("Repeat password: ")

password1 = password1.encode()

passwd = encryptor(password1,sha1(password1).digest()).encrypt((passwd+"unencrypted").encode())

with open(f"data{sl}key{sl}{name}.key", "wb") as f:
    f.write(passwd)
    f.close()

passwd = password1 = password2 = (len(max(passwd,password1))*2) * "A"

print(f"{name} room has been generated and encrypted")