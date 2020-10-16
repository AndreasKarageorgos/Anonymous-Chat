from hashlib import sha512

def auth(uname,passwd,members):
    sl = "/"
    try:
        with open(f"conf{sl}banned","r") as f:
            banned = f.read().split("\n")
            f.close()
    except FileNotFoundError:
        banned = []

    comp = sha512(uname+passwd).hexdigest()
    try:
        uname = uname.decode()
    except UnicodeDecodeError:
        return False
    if (uname in members and members[uname] == comp) and (uname not in banned):
        return True
    return False