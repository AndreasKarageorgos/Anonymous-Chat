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



"""
MIT License

Copyright (c) 2020 AndreasKarageorgos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""