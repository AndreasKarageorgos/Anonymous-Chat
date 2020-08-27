from hashlib import sha512

def auth(uname,passwd,members):
    comp = sha512(uname+passwd).hexdigest()
    try:
        uname = uname.decode("ascii")
    except UnicodeDecodeError:
        return False
    if uname in members and members[uname] == comp:
        return True
    return False