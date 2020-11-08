from hashlib import sha1
from getpass import getpass
from data.libraries.AES_cryptography import decryptor
from data.libraries.rooms import Rooms

sl = "/"

key = Rooms()

if not key:
    exit()

password = getpass("Key Password: ").encode()

try:
    with open(key, "rb") as f:

        plainkey = decryptor(password,sha1(password).digest()).decrypt(f.read())
        if not plainkey.endswith(b"unencrypted"):
            f.close()
            print("Wrong password.")
            exit()
        f.close()

    name = key.split(sl)[-1][:len(".key")*-1]
    print(name)

    with open(f"{name}.key.unsafe", "wb") as f:
        f.write(plainkey[:len("unencrypted")*-1])
        f.close()

    print("Key has been extracted. This key is not encrypted.")

except FileNotFoundError:
    print("Key.key file did not found")