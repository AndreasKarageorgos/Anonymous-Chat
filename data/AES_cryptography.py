#Coded by Andreas Karageorgos

from Crypto.Cipher import AES
from hashlib import sha256
from string import ascii_letters


def pad_message(message):
    message = message.decode("ascii")
    while (len(message)%16 !=0):
        message+=" "
    return message.encode("ascii")

class encryptor():

    def __init__(self,key,IV):
        self.key = sha256(key).digest()
        self.mode = AES.MODE_CBC
        self.IV = sha256(IV).digest()[:16]
        self.cipher = AES.new(self.key,self.mode,self.IV)

    def encrypt(self,text):
        self.text = pad_message(text)
        self.ciphertext = self.cipher.encrypt(self.text)
        self.text = "A"*(len(self.text)+1)*100 #Ovverite text in memory
        del self.text #Deletes text from memory
        return self.ciphertext

class decryptor():
    
    def __init__(self,key,IV):
        self.key = sha256(key).digest()
        self.mode = AES.MODE_CBC
        self.IV = sha256(IV).digest()[:16]
        self.cipher = AES.new(self.key,self.mode,self.IV)

    
    def decrypt(self,ciphertext):
        self.plaintext = self.cipher.decrypt(ciphertext).strip()
        ciphertext
        del ciphertext
        return self.plaintext


