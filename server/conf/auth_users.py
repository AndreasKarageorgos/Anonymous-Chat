from hashlib import sha512

def auth(uname,passwd,members,whitelist):
    sl = "/"

    try:
        if whitelist:
            with open(f"conf{sl}whitelist","r") as f:
                alist = f.read().split("\n")
                f.close()
            if uname.decode() not in alist:
                return False
    except FileNotFoundError:
        alist = []
    except UnicodeDecodeError:
        return False

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
    if (uname in members and members[uname] == comp) and (uname not in banned or uname==b":"):
        return True
    return False