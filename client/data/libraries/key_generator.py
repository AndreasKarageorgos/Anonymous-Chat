from random import randint, choice
from tkinter import messagebox
from getpass import getpass
from hashlib import sha1
from sys import maxunicode
try:
    from data.libraries.AES_cryptography import encryptor
    from data.libraries.askpass import askpass
except:
    from AES_cryptography import encryptor
    from askpass import askpass
from platform import uname
from string import ascii_letters, digits, whitespace


def key_generator():

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


    try:
        name = askpass(True).strip()
    except AttributeError:
        return
    
    while name=="":
        name = askpass(True).strip()


    passwd = "".join(chars)


    password1 = askpass()

    if password1 == None:return

    while password1=="":
        password1 = askpass()
    password2 = askpass()

    if password2 == None:return

    while password1!=password2:
        #print("Passwords do not match.")
        messagebox.showerror(title="Error", message="Passwords do not match.")
        password1 = askpass()
        if password1 == None:return
        while password1=="":
            if password1 == None:return
            password1 = askpass()
        password2 = askpass()
        if password2== None:return


    password1 = password1.encode()

    passwd = encryptor(password1,sha1(password1).digest()).encrypt((passwd+"unencrypted").encode())

    with open(f"data{sl}key{sl}{name}.key", "wb") as f:
        f.write(passwd)
        f.close()

    passwd = password1 = password2 = (len(max(passwd,password1))*2) * "A"

    print(f"{name} room has been generated and encrypted.\nClick the \"R\" button to refresh !")