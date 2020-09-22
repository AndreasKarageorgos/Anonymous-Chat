from getpass import getpass
from hashlib import sha1
from data.libraries.AES_cryptography import encryptor

keypath = input("Drag and drop the key file here:")

if keypath[0] == "'" or keypath[0] == '"':
    keypath = keypath[1:-2]
    print(keypath)

while not keypath.endswith(".key") and not keypath.endswith(".unsafe"):
    keypath = input("Drag and drop the key file here:")


with open(keypath,"rb") as f:
    key = f.read()
    f.close()

if keypath.endswith(".key"):
    with open("data/key/Key.key","wb") as f:
        f.write(key)
        f.close()
else:
    password1 = getpass("Setup a password: ") or "sodqkwi2"
    password2 = getpass("Repeat password: ") or "mgh82fl"
    while password1!=password2:
        print("passwords do not match\n")
        password1 = getpass("Setup a password: ") or "sodqkwi2"
        password2 = getpass("Repeat password: ") or "mgh82fl"

    
    password1 = password1.encode("ascii")

    with open("data/key/Key.key", "wb") as f:
        cipherkey = encryptor(password1,sha1(password1).digest()).encrypt((key+b"unencrypted"))
        f.write(cipherkey)
        f.close()

keypath=key=password1=password2=cipherkey = "A"*2048

del keypath,key,password1,password2,cipherkey

print("Key loaded. You can now use the chat.")

