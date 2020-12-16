from random import randint, choice
from getpass import getpass
from hashlib import sha1
from sys import maxunicode
from data.libraries.AES_cryptography import encryptor
from platform import uname
from string import ascii_letters, digits, whitespace


if uname()[0].lower().startswith("win"):
    sl = "\\"
else:
    sl = "/"
    
passwd = ""


counter = 0
chars = []


while counter<=44:
    try:
        temp = chr(randint(0,maxunicode))
        le = len(temp.encode())
        if le<=4 and not(temp in whitespace):
            chars.append(temp)
            counter+=le
    except UnicodeEncodeError:
        pass

if counter<48:
    seats = 48-counter
    for _ in range(seats):
        chars.append(choice(ascii_letters+digits))

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