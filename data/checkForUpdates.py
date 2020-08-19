#Coded by Andreas Karageorgos

import requests

def check():
    prox = {
        "https": "socks5://127.0.0.1:9050"
    }  

    program = "https://github.com/AndreasKarageorgos/Anonymous-Chat"

    server = "Alpha 1.0.2"
    client = "Alpha 1.0.1"
    
    try:
        r = requests.get("https://raw.githubusercontent.com/AndreasKarageorgos/Anonymous-Chat/master/VERSIONS", proxies = prox).text.split()
    except:
        return "Connection to Tor network could not be established."
    
    sv = r[1]+" "+r[2]
    cv = r[1]+" "+r[5]

    if (sv!=server and cv!=client):
        return f"Update found for client and server !!!\n\nYou can download it here => {program}"
    elif(sv!=server):
        return f"Update found for server !!!\n\nYou can download it here {program}"
    elif(cv!=client):
        return f"Update found for client !!!\n\nYou can download it here {program}"
    
    return"No updates found !!!"

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