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

version = "Beta 1.0"

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
max_clients = 10     #Change this to make your server bigger or smaller

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip,server_port))
server_socket.settimeout(0.2)
server_socket.listen(max_clients)

rooms = {}

broken_pipe_list = []
#This is to stop the threads when the server is closed
global dead
dead = False

def accept_connections():

    global dead
    while not dead:
        try:
            client,_ = server_socket.accept()
            client.settimeout(3)
            data = client.recv(1024)
            if data == b"online":
                client.send("True".encode("ascii"))
                client.close()
                data = ""
            data = data.split(b":")
            if 3<=len(data)<=4 :
                if data[0] == b"register" and b"server" not in data[1].lower():
                    resp = register_users.reg_user(data[1],data[2],members)
                    if resp: 
                        client.send("True".encode("ascii"))
                        print(data[1],"Registered !")
                    else:
                        client.send("False".encode("ascii"))
                elif data[0] == b"login" and len(data)==4:
                    resp = auth_users.auth(data[1],data[2],members)
                    if resp:
                        client.send("True".encode("ascii"))
                        print(data[1],"Logged in")
                        keyword = data[-1]

                        if keyword in rooms:
                            rooms[keyword].update({data[1].decode("ascii"):client})
                        else:
                            rooms.update({ keyword:{data[1].decode("ascii"):client}})
                        
                        time.sleep(0.1)
                        broadcast("Server",data[1].decode("ascii")+" Logged in",keyword)

                    else:
                        client.send("False".encode("ascii"))
                    

        except:
            pass

def broadcast(name,message,key=None):

    if name=="Server" and key==None:
        for k in rooms:
            for client in rooms[k]:
                try:
                    rooms[k][client].settimeout(0.2)
                    rooms[k][client].send(f"Server:{message}".encode("ascii"))
                except:
                    if client not in [j[1] for j in remove_clients]:
                        remove_clients.append((k,client,False))
        return
    
    if name=="Server":
        for client in rooms[key]:
            try:
                rooms[key][client].settimeout(0.2)
                rooms[key][client].send(f"Server:{message}".encode("ascii"))
            except:
                if client not in [j[1] for j in remove_clients]:
                        remove_clients.append((key,client,False))
        return
    
    for client in rooms[key]:
        try:
            rooms[key][client].settimeout(0.2)
            rooms[key][client].send(b"%s:%s" % (name.encode("ascii"), message) )
        except:
            if client not in [j[1] for j in remove_clients]:
                remove_clients.append((key,client,False))

global remove_clients
remove_clients = [] 

def recv_message():
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
                            if message == b"COMMAND:D":
                                rooms[key][client].close()
                                print(client, "logged off")
                                remove_clients.append((key,client,True))
                            elif message == b"COMMAND:S":
                                particiapnts = ",".join([x for x in rooms[key]])
                                try:rooms[key][client].send(f"Server:{particiapnts}".encode("ascii"))
                                except:remove_clients.append((key,client,False))
                            else:
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


print("Closing the server !")
dead = True
time.sleep(2)
kill_all_connections()
server_socket.close()
print("Server closed.")

