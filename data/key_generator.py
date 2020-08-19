#Coded by Andreas Karageorgos

from random import randint
from string import ascii_letters,digits

passwd = ""
IV = ""

chars = list(ascii_letters+digits+"~`!@#$%^&*()_+-={}[]\\:;'\"<>,./?")

l = len(chars)-1

#mixing chars
for _ in range(randint(50,100)):
    n1 = randint(0,l)
    n2 = randint(0,l)
    chars[n1], chars[n2] = chars[n2], chars[n1]

#creating passwd

passwd = "".join([chars[randint(0,l)] for _ in range(randint(100,256))])

#creating IV

IV = "".join([chars[randint(0,l)] for _ in range(16)])

print("Password and IV have ben generated !!!\n")
ans = input("Do you want to replace the key files ? [y/n]: ")
while ans != "y" and ans!="n":
    ans = input("Do you want to replace or create the files ? [y/n]: ")

if ans == "y":
    with open("key/AES.key", "w") as f:
        f.write(passwd)
        f.close()
    with open("key/IV.key", "w") as f:
        f.write(IV)
        f.close()

    print("Done !")


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