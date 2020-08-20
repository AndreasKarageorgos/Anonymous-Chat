#Coded by Andreas Karageorgos

import requests

def check():
    prox = {
        "https": "socks5://127.0.0.1:9050"
    }  

    program = "https://github.com/AndreasKarageorgos/Anonymous-Chat"

    server = "Alpha 1.1"
    client = "Alpha 1.1"
    
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