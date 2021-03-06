#Coded by Andreas Karageorgos

from Crypto.Cipher import AES
from hashlib import sha256
from string import ascii_letters


def pad_message(message):
    while (len(message)%16 !=0):
        message+=b" "
    return message

class encryptor():

    def __init__(self,key,IV):
        if len(key)==32:
            self.key = key
        else:
            self.key = sha256(key).digest()
        self.mode = AES.MODE_CBC
        if len(IV)==16:
            self.IV = IV
        else:    
            self.IV = sha256(IV).digest()[:16]
        self.cipher = AES.new(self.key,self.mode,self.IV)

    def encrypt(self,text):
        self.text = pad_message(text)
        self.ciphertext = self.cipher.encrypt(self.text)
        self.text = "A"*(len(self.text)+1)*100 #overwrite text
        del self.text #Deletes text from memory
        return self.ciphertext

class decryptor():
    
    def __init__(self,key,IV):
        if len(key)==32:
            self.key = key
        else:
            self.key = sha256(key).digest()
        self.mode = AES.MODE_CBC
        if len(IV)==16:
            self.IV = IV
        else:
            self.IV = sha256(IV).digest()[:16]
        self.cipher = AES.new(self.key,self.mode,self.IV)

    
    def decrypt(self,ciphertext):
        self.plaintext = self.cipher.decrypt(ciphertext).strip()
        ciphertext
        del ciphertext
        return self.plaintext


