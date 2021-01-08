from getpass import getpass
from hashlib import sha1
from data.libraries.AES_cryptography import encryptor
from platform import uname
from string import whitespace



print("You can load keys that end to .unsafe or .key\nA .unsafe file is going to be encrypted and a .key file is going to be loaded as it is.")


if uname()[0].lower().startswith("win"):
    sl = "\\"
else:
    sl = "/"


keypath = input("Drag and drop the key file here:")

if keypath[0] == "'" or keypath[0] == '"':
    keypath = keypath[1:-2]

while not keypath.endswith(".key") and not keypath.endswith(".unsafe"):
    keypath = input("Drag and drop the key file here:")


with open(keypath,"rb") as f:
    key = f.read()
    f.close()

name = keypath.split(sl)[-1].split(".")[0]    

if keypath.endswith(".key"):
    with open(f"data{sl}key{sl}{name}.key","wb") as f:
        f.write(key)
        f.close()
    del keypath,key
else:
    password1 = getpass("Setup a password: ")
    password2 = getpass("Repeat password: ")
    while password1!=password2 or password1 in whitespace or password2 in whitespace:
        print("passwords do not match\n")
        password1 = getpass("Setup a password: ")
        password2 = getpass("Repeat password: ")

    
    password1 = password1.encode()

    with open(f"data{sl}key{sl}{name}.key", "wb") as f:
        cipherkey = encryptor(password1,sha1(password1).digest()).encrypt((key+b"unencrypted"))
        f.write(cipherkey)
        f.close()

    password2 = password1
    keypath = keypath.encode()
    keypath=key=password1=password2=cipherkey = (len(max(keypath,key,password1,cipherkey)*2)) * "A"

    del keypath,key,password1,password2,cipherkey

print("Key loaded. You can now use the chat.")

