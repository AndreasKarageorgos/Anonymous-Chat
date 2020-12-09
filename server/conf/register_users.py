from hashlib import sha512
from platform import uname as sysname

def reg_user(uname,passwd,users,whitelist):

    if sysname()[0].lower().startswith("win"):
        sl = "\\"
    else:
        sl = "/"

    alist = []

    if whitelist:
        try:
            with open(f"conf{sl}whitelist","r") as f:
                alist = f.read().split("\n")
                f.close()
        except FileNotFoundError:
            open(f"conf{sl}whitelist","w").close()


    try:
        if whitelist and (uname.decode() not in alist):
            return False
    except UnicodeDecodeError:
        return False      
    
    if b" " in uname or b"\n" in uname or b":" in uname:
        return False
    with open(f"conf{sl}users","a") as f:
        try:
            comp = sha512(uname+passwd).hexdigest()
            uname = uname.decode()
            if uname.lower() not in [x.lower() for x in users]:
                f.write(f"{uname}:{comp}\n")
                users.update({uname:comp})
                return True
            return False
        except UnicodeDecodeError:
            return False
