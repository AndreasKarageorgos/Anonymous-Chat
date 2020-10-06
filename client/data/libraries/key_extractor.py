from hashlib import sha1
from getpass import getpass
from data.libraries.AES_cryptography import decryptor

sl = "/"

password = getpass("Key Password: ").encode("ascii")

try:
    with open(f"data{sl}key{sl}Key.key", "rb") as f:

        plainkey = decryptor(password,sha1(password).digest()).decrypt(f.read())
        if not plainkey.endswith(b"unencrypted"):
            f.close()
            print("Wrong password.")
            exit()
        f.close()
    
    with open("Key.key.unsafe", "wb") as f:
        f.write(plainkey[:len("unencrypted")*-1])
        f.close()

    print("Key has been extracted. This key is not encrypted.")

except FileNotFoundError:
    print("Key.key file did not found")