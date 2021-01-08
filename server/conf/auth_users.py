from hashlib import sha512
from platform import uname as sysname



def auth(uname,passwd,members,whitelist):
    
    if sysname()[0].lower().startswith("win"):
        sl = "\\"
    else:
        sl = "/"

    alist = []

    try:
        if whitelist:
            with open(f"conf{sl}whitelist","r") as f:
                alist = f.read().split("\n")
                f.close()
            if uname.decode() not in alist:
                return False
    except FileNotFoundError:
        return False
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