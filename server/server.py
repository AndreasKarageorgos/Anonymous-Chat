#coded by Andreas Karageorgos
#GitHub: https://github.com/AndreasKarageorgos/

import socket
import threading
import requests
from random import randint
from string import ascii_letters
from conf import register_users,auth_users
from hashlib import sha512
import time

#Checks for updates

global sl
sl = "/"


version = "version 0.3.2"

def update(version):
    prox = {
        "https": "socks5://127.0.0.1:9050"
    }  

    program = "https://github.com/AndreasKarageorgos/SPC-Chat/ \n"
    
    try:
        r = requests.get("https://raw.githubusercontent.com/AndreasKarageorgos/SPC-Chat/master/VERSIONS", proxies = prox).text.split()
    except:
        return "Connection to Tor network could not be established."
    
    sv = r[1]+" "+r[2]

    if(sv!=version):
        return f"Update found for server !!!\n\nYou can download it here {program}"
    
    return"No updates found !!!"
print(update(version))


#Load config file.

while True:
    try:
        with open("config.config","r") as f:
            config_file = f.read().strip()
            f.close()
        config_file = config_file.split("\n")
        config = {}
        for i in config_file:
            config.update({i.split("=")[0]: i.split("=")[1]})
        break
    except FileNotFoundError:
        with open("config.config","w") as f:
            f.write("message=Wealcome To the server\nmax_clients=-1")
            f.close()


#loads members

members = {}

try:
    f=open(f"conf{sl}users","r")
    temp = f.read().split("\n")
    for i in temp:
        temp2 = i.split(":")
        name = temp2[0]
        hash_ = ":".join(temp2[1:])
        members.update({name:hash_})
except FileNotFoundError:
    open(f"conf{sl}users","w").close()

#Creating sockets

server_ip = "127.0.0.1" #Do not change !!! (Unless you know what you are doing)
server_port = 4488
max_clients = int(config["max_clients"].strip())

#Buff size of client is 100 
server_message = config["message"].strip()[:93]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        server_socket.bind((server_ip,server_port))
        break
    except KeyboardInterrupt:
        exit()
    except OSError:
        print("The port 4488 is already in use\nTry to close the programm that is using this port.")
        exit()

server_socket.settimeout(0.2)
server_socket.listen()

rooms = {}
spamm = {}

broken_pipe_list = []
#This is to stop the threads when the server is closed
global dead
dead = False

def accept_connections():

    def maxed():
        counter = 0
        for room in rooms:
            counter+=len(rooms[room])
        if counter==max_clients:
            return True
        return False


    global dead
    while not dead:
        try:
            if maxed==-1 or not maxed():
                client,_ = server_socket.accept()
                client.settimeout(3)
                data = client.recv(181)
                if data == b"online":
                    client.send("True".encode())
                    client.close()
                    data = ""
                data = data.split(b":")
                if len(data)>=3:
                    if data[0] == b"register" and b"server" not in data[1].lower():
                        data[2] = b":".join(data[2:])
                        resp = register_users.reg_user(data[1],data[2],members)
                        if resp: 
                            client.send("True".encode())
                            print(data[1].decode(),"Registered !")
                        else:
                            client.send("False".encode())
                    elif data[0] == b"login" and len(data)>=4:
                        if len(data) == 4:
                            resp = auth_users.auth(data[1],data[2],members)
                        else:
                            resp = auth_users.auth(data[1],b":".join(data[2:-1]),members)
                        if resp:
                            client.send("True".encode())
                            print(data[1].decode(),"Logged in")
                            spamm.update({data[1]:time.time()})
                            keyword = data[-1]

                            if keyword in rooms:
                                rooms[keyword].update({data[1].decode():client})
                            else:
                                rooms.update({ keyword:{data[1].decode():client}})
                            
                            time.sleep(0.2)
                            client.send(b"Server:%s" % server_message.encode())
                            time.sleep(0.1)
                            broadcast("Server",data[1].decode()+" Logged in",keyword)

                        else:
                            client.send("False".encode())
                    

        except:
            pass

def broadcast(name,message,key=None):

    if name=="Server" and key==None:
        for k in rooms:
            for client in rooms[k]:
                try:
                    rooms[k][client].settimeout(0.2)
                    rooms[k][client].send(f"Server:{message}".encode())
                except:
                    if client not in [j[1] for j in remove_clients]:
                        remove_clients.append((k,client,False))
        return
    
    if name=="Server":
        for client in rooms[key]:
            try:
                rooms[key][client].settimeout(0.2)
                rooms[key][client].send(f"Server:{message}".encode())
            except:
                if client not in [j[1] for j in remove_clients]:
                        remove_clients.append((key,client,False))
        return
    
    for client in rooms[key]:
        try:
            rooms[key][client].settimeout(0.2)
            rooms[key][client].send(b"%s:%s" % (name.encode(), message) )
        except:
            if client not in [j[1] for j in remove_clients]:
                remove_clients.append((key,client,False))

global remove_clients
remove_clients = [] 

def recv_message():

    def close(key,client):
        rooms[key][client].close()
        print(client, "logged off")
        remove_clients.append((key,client,True))
    
    def partici(key,client):
        particiapnts = ",".join([x for x in rooms[key]])
        if len("Server:"+particiapnts)<=335:
            try:rooms[key][client].send(f"Server:{particiapnts}".encode())
            except:remove_clients.append((key,client,False))
        else:
            try:rooms[key][client].send("Server: There are too many people on this room to be displayed.")
            except:remove_clients.append((key,client,False))

    commands = {b"COMMAND:D":close,b"COMMAND:S":partici}

    global remove_clients
    global dead
    while not dead:
        try:
            if(len(rooms)>0):
                for key in rooms:
                    for client in rooms[key]:
                        try:
                            rooms[key][client].settimeout(0.1)
                            message = rooms[key][client].recv(160)
                            if len(message)>80:
                                print(client,"Send message over 80 bytes.")
                                remove_clients.append((key,client,False))
                            elif round(time.time()-spamm[client.encode()], 2) < 1.5:
                                remove_clients.append((key,client,False))
                                print(client,"got kicked for spamming")
                            else:
                                spamm[client.encode()] = time.time()
                            try:
                                commands[message](key,client)
                            except:
                                broadcast(name=client, message=message, key=key)
                        except:
                            pass
            
            for pair in remove_clients:
                try:
                    rooms[pair[0]].pop(pair[1])
                    if len(rooms[pair[0]]) == 0:
                        rooms.pop(pair[0])
                    if pair[2]:
                        broadcast(name="Server",message=f"{pair[1]}, logged off",key=pair[0])
                    else:
                        broadcast(name="Server",message=f"{pair[1]}, lost connection",key=pair[0])
                        print(pair[1], "lost connection")
                    print(pair[1],"logged off")
                except:
                    pass
        except RuntimeError:
            pass
        
        remove_clients = []

def kill_all_connections():
    for key in rooms:
        for client in rooms[key]:
            try:
                rooms[key][client].close()
            except:
                pass


threading.Thread(target=accept_connections).start()
threading.Thread(target=recv_message).start()


#Server Commands

def kick(username):
    for k in rooms:
        if username in rooms[k]:
            if username not in [j[1] for j in remove_clients]:
                remove_clients.append((k,username,True))
            break

def helpme(*_):
    print("""
    1.help --This help menu
    2.kick (name) --Kicks a member of the server
    3.ban (name) --Bans a member from the server
    4.stop  --Stops the server
    """)

def ban(username):
    global sl
    if username in members:
        with open(f"conf{sl}banned","a") as f:
            f.write(username+"\n")
            f.close()
        print(username,"Banned")
        kick(username)
    else:
        print("This username does not exists")

print("Server is running ! Type help for a list of help menu.")

commands = {"kick":kick,"help":helpme,"ban":ban}
try:
    command = input("")
    while command.lower() != "stop":
        command = command.split()
        command.append("_")
        if(command[0] in commands):
            commands[command[0]](command[1])
        else:
            print("CONSOLE: Command did not found!")
        command = input("")
except KeyboardInterrupt:
    pass


broadcast("Server","Server closed !")
print("Closing open connections.")
dead = True
time.sleep(2)
kill_all_connections()
server_socket.close()
print("Server closed.")

