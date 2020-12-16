#coded by Andreas Karageorgos
#GitHub: https://github.com/AndreasKarageorgos/

import socket
import threading
import requests
from random import randint, choice
from string import ascii_letters, digits
from conf import register_users,auth_users
from hashlib import sha512, sha256
import time
from platform import uname as sysname

def main():
    global sl
    if sysname()[0].lower().startswith("win"):
        sl = "\\"
    else:
        sl = "/"



    #Checks for updates


    version = "version 1.5"

    def update(version):
        prox = {
            "https": "socks5://127.0.0.1:9050"
        }  

        program = "https://github.com/AndreasKarageorgos/SPC-Chat/ \n"
        
        try:
            r = requests.get("https://raw.githubusercontent.com/AndreasKarageorgos/SPC-Chat/master/VERSIONS", proxies = prox).text.split()
        except:
            return "Failed"
        
        sv = r[1]+" "+r[2]

        if(sv!=version):
            return f"Update found for server !!!\n\nYou can download it here {program}"
        
        return "No updates found !!!"
    
    utemp = update(version)

    if utemp == "Failed":
        print("Failed to connect to Tor\n")
        return
    else:
        print(utemp)

    del utemp

    #Load config file.

    while True:
        try:
            with open("server.config","r") as f:
                config_file = f.read().strip()
                f.close()
            config_file = config_file.split("\n")
            config = {}
            for i in config_file:
                config.update({i.split("=")[0]: i.split("=")[1]})
            break
        except FileNotFoundError:
            with open("server.config","w") as f:
                f.write("message=Wealcome To the server\nmax_clients=-1\nprivate=false\nwhite_list=false\n")
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
    private_server = config["private"].strip().lower()
    try:
        whitelist = config["white_list"].strip().lower()
    except KeyError:
        whitelist = "false"
        print("Please delete the config file and restart the server to load the new option.")


    if private_server == "true":
        private_server = True
    else:
        private_server = False

    if whitelist == "true":
        whitelist = True
    else:
        whitelist = False

    if private_server:
        private_key = sha256("".join([choice(ascii_letters+digits) for _ in range(randint(50,100))]).encode()).digest()
    #Buff size of client is 100 
    server_message = config["message"].strip()[:93]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            server_socket.bind((server_ip,server_port))
            break
        except KeyboardInterrupt:
            return
        except OSError:
            print("The port 4488 is already in use\nTry to close the programm that is using this port.")
            return

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
                    data = client.recv(108)
                    if data == b"online":
                        client.send("True".encode())
                        client.close()
                        data = ""
                        
                    if private_server and data == b"private":
                        time.sleep(0.2)
                        client.send(private_key)
                        client.close()
                        data = ""
                    elif data == b"private":
                        client.send("0".encode())
                        client.close()
                

                    if 36<=len(data)<=44:
                        temp = data
                        data = []
                        data.append(temp[:2])
                        t1 = (10-(44-len(temp)))+2
                        data.append(temp[2:t1])
                        data.append(temp[t1:])
                    elif 100<=len(data)<=108:
                        temp = data
                        data = []
                        data.append(temp[:2])
                        t1 = (10-(108-len(temp)))+2
                        data.append(temp[2:t1])
                        data.append(temp[t1:t1+32])
                        data.append(temp[t1+32:])
                    else:
                        data=""


                    if len(data)>=3:
                        if data[0] == b"rg" and b"server" not in data[1].lower():
                            resp = register_users.reg_user(data[1],data[2],members,whitelist)
                            if resp: 
                                client.send("True".encode())
                                print(data[1].decode(),"Registered !")
                            else:
                                client.send("False".encode())
                        elif data[0] == b"lg":
                            resp = auth_users.auth(data[1],data[2],members,whitelist)
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
                                elif round(time.time()-spamm[client.encode()], 2) < 1.8:
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
        1.help              -- This help menu
        2.kick (name)       -- Kicks a member of the server
        3.ban (name)        -- Bans a member from the server
        4.stop              -- Stops the server
        5.whiteadd (name)   -- adds a client to the whitelist
        6.whiterm (name)    -- removes a client from the whitelist
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


    def whiteadd(name):
        if name!="_":
            try:
                with open(f"conf{sl}whitelist","r+") as f:
                    tlist = f.read().split("\n")
                    if name not in tlist:
                        f.write(name+"\n")
                        print(f"added {name} to the whitelist")
                    else:
                        print(f"{name} already in whitelist")
                    f.close()
            except FileNotFoundError:
                with open(f"conf{sl}whitelist", "w") as f:
                    f.write(name+"\n")
                    f.close()
                print(f"added {name} to the whitelist")
        else:
            print("type help for the help menu")

    def whiterm(name):
        if name!="_":
            try:
                with open(f"conf{sl}whitelist","r+") as f:
                    tlist = f.read().split("\n")
                    if name in tlist:
                        tlist.remove(name)
                        f.close()
                        with open(f"conf{sl}whitelist","w") as f:
                            for i in tlist:
                                if len(i.strip())>0:
                                    f.write(i.strip()+"\n")
                                    f.flush()
                            f.close()
                        print(f"{name} removed from whitelist")
                    else:
                        print(f"{name} not in whitelist")
            except FileNotFoundError:
                print(f"{name} not in whitelist.")



    print("Server is running ! Type help for a list of help menu.")

    commands = {"kick":kick,"help":helpme,"ban":ban,"whiteadd":whiteadd,"whiterm":whiterm}
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

main()