from hashlib import sha512

def reg_user(uname,passwd,users):

    sl = "/"

    if b" " in uname or b"\n" in uname:
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
