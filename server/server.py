#Coded by Andreas Karageorgos

import socket
import threading
import requests
from random import randint
from string import ascii_letters
from conf import register_users,auth_users
from hashlib import sha512
import time

#Checks for updates

version = "Alpha 2.0"
def update(version):
    prox = {
        "https": "socks5://127.0.0.1:9050"
    }  

    program = "https://github.com/AndreasKarageorgos/Anonymous-Chat \n"
    
    try:
        r = requests.get("https://raw.githubusercontent.com/AndreasKarageorgos/Anonymous-Chat/master/VERSIONS", proxies = prox).text.split()
    except:
        return "Connection to Tor network could not be established."
    
    sv = r[1]+" "+r[2]

    if(sv!=version):
        return f"Update found for server !!!\n\nYou can download it here {program}"
    
    return"No updates found !!!"
print(update(version))

#loads members

members = {}

try:
    f=open("conf/users","r")
    temp = f.read().split("\n")
    for i in temp:
        temp2 = i.split(":")
        name = temp2[0]
        hash_ = ":".join(temp2[1:])
        members.update({name:hash_})
except FileNotFoundError:
    open("conf/users","w").close()

#Creating sockets

server_ip = "127.0.0.1" #Do not change !!! (Unless you know what you are doing)
server_port = 4488
max_clients = 5     #Change this to make your server bigger or smaller

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip,server_port))
server_socket.settimeout(0.2)
server_socket.listen(max_clients)

server_message = "Wealcome !!!"

clients = {}
broken_pipe_list = []
#This is to stop the threads when the server is closed
global dead
dead = False


def accept_connections():

    global dead
    while not dead:
        try:
            client,_ = server_socket.accept()
            client.settimeout(1)
            data = client.recv(1024)
            data = data.split(b":")
            if len(data) ==3:
                if data[0] == b"register":
                    resp = register_users.reg_user(data[1],data[2],members)
                    if resp: 
                        client.send("True".encode("ascii"))
                        print(data[1],"Registered !")
                    else:
                        client.send("False".encode("ascii"))
                elif data[0] == b"login":
                    resp = auth_users.auth(data[1],data[2],members)
                    if resp:
                        client.send("True".encode("ascii"))
                        print(data[1],"Logged in")
                        try:
                            clients.update({data[1].decode("ascii"):client})
                            client.send(f"Server:{server_message}".encode("ascii"))
                        except UnicodeDecodeError:
                            pass

                    else:
                        client.send("False".encode("ascii"))
        except:
            pass

def broadcast(message):
    for key in clients:
        try:
            clients[key].send(message)
        except BrokenPipeError:
            if key not in broken_pipe_list:
                broken_pipe_list.append(key)
        except:
            if key not in broken_pipe_list:
                broken_pipe_list.append(key)

def recv_message():
    
    global dead
    while not dead:
        broken_pipe_list = []
        if(len(clients)>0):
            try:
                for key in clients:
                    try:
                        clients[key].settimeout(0.2)
                        message = clients[key].recv(160)
                        if (len(message)<=80):
                            if(len(message)>0 and message!=b"\n"):
                                if (b"COMMAND:D" in message):
                                    print(key,"logged off")
                                    broadcast(f"Server: {key} logged off".encode("ascii")) #optional
                                    broken_pipe_list.append(key)
                                else:
                                    broadcast(b"%s:%s" % (key.encode("ascii"),message))
                                    print(key,f"Send a message of {len(message)} bytes")
                        else:
                            broadcast(f"Server: {key} kicked for flooding the server.".encode("ascii"))
                            print(key,f"Kicked for sending message of {len(message)} bytes")
                    except BrokenPipeError:
                        if key not in broken_pipe_list:
                            broken_pipe_list.append(key)
                    except:
                        pass
            except RuntimeError:
                pass
        for br in broken_pipe_list:
            try:
                del clients[br]
            except:
                pass


threading.Thread(target=accept_connections).start()
threading.Thread(target=recv_message).start()


#Server Commands

def kick(username):
    if (username in clients):
        clients[username].close()
        return
    print("Name did not found")

def helpme(*_):
    print("""
    1.help --This help menu
    2.kick (name) --Kicks a member of the server
    3.stop  --Stops the server
    """)

print("Server is running ! Type help for a list of help menu.")

commands = {"kick":kick,"help":helpme}
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


print("Server Stopped !")
dead = True
server_socket.close()

