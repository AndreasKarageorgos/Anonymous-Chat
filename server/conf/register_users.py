from hashlib import sha512

def reg_user(uname,passwd,users):
    with open("conf/users","a") as f:
        try:
            comp = sha512(uname+passwd).hexdigest()
            uname = uname.decode("ascii")
            if uname not in users:
                f.write(f"{uname}:{comp}\n")
                users.update({uname:comp})
                return True
            return False
        except UnicodeDecodeError:
            return False
