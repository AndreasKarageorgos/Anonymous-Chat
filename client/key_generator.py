from random import randint
from string import ascii_letters,digits
from getpass import getpass
from hashlib import sha1
from data.libraries.AES_cryptography import encryptor

sl = "/"

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


password1 = getpass("Set up a password: ") or "nfjeiqodc"
password2 = getpass("Repeat password: ") or "ldiqmvbr"

while password1!=password2:
    print("Passwords do not match.")
    password1 = getpass("Set up a password: ") or ""
    password2 = getpass("Repeat password: ")

password1 = password1.encode()

passwd = encryptor(password1,sha1(password1).digest()).encrypt((passwd+"unencrypted").encode())

print("Key has been generated and encrypted")

with open(f"data{sl}key{sl}Key.key", "wb") as f:
    f.write(passwd)
    f.close()