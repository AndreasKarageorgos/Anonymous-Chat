#Coded by Andreas Karageorgos

import socket
import threading
from random import randint
from string import ascii_letters
from data import checkForUpdates
import time

#Checks for updates

print("Checking for updates...\n")

print(checkForUpdates.check()+"\n")

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

    def random_username():
        username = ""
        for _ in range(randint(6,12)):
            if randint(0,5) == 0:
                username+=str(randint(0,9))
            username+=ascii_letters[randint(0,len(ascii_letters)-1)]
        return username
    
    global dead
    while not dead:
        try:
            client,_ = server_socket.accept()
            assigned_username = random_username()
            
            while assigned_username in clients:
                assigned_username = random_username()
            try:
                client.send(f"Server: {server_message}\nYour username is: {assigned_username}\n".encode("ascii"))
                print(assigned_username,"logged in!")
                broadcast(f"Server: {assigned_username} joined the server !\n".encode("ascii")) #Optional 
                clients.update({assigned_username:client})
            except:
                print("Error in lines 46-49")
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
                        message = clients[key].recv(80)
                        if(len(message)>0 and message!=b"\n"):
                            if (b"COMMAND:D" in message):
                                print(key,"logged off")
                                broadcast(f"Server: {key} logged off\n".encode("ascii")) #optional
                                broken_pipe_list.append(key)
                            else:
                                broadcast(b"%s:%s" % (key.encode("ascii"),message))
                                print(key,f"Send a message of {len(message)} bytes")
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