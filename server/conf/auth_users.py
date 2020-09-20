from hashlib import sha512

def auth(uname,passwd,members):

    try:
        with open("conf/banned","r") as f:
            banned = f.read().split("\n")
            f.close()
    except FileNotFoundError:
        banned = []

    comp = sha512(uname+passwd).hexdigest()
    try:
        uname = uname.decode("ascii")
    except UnicodeDecodeError:
        return False
    if (uname in members and members[uname] == comp) and (uname not in banned):
        return True
    return False