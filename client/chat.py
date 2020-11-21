#coded by Andreas Karageorgos
#GitHub: https://github.com/AndreasKarageorgos/

import tkinter as tk
from tkinter import Entry as tk_Entry , Text as tk_Text,Label as tk_Label, Button as tk_Button, messagebox as tk_messagebox, Frame as tk_Frame
from data.libraries import AES_cryptography, servers, loadServers
from data.libraries.register import register
from data.libraries.torSocks import torSocks
from data.libraries.rooms import Rooms 
from random import choice
from string import ascii_letters,digits
from hashlib import sha256,sha512,sha1
from os import getcwd
import requests
import webbrowser
import socks
import threading
import time
import getpass

def center_window(window,width_of_window,height_of_window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))


global sl
sl = "/"

#Checks for updates


version = "version 1.4"

def update(version):

    prox = {
        "https": "socks5://127.0.0.1:9050"
    }  

    program = "https://github.com/AndreasKarageorgos/SPC-Chat/ \n"
    
    try:
        r = requests.get("https://raw.githubusercontent.com/AndreasKarageorgos/SPC-Chat/master/VERSIONS", proxies = prox).text.split()
    except:
        return "Connection to Tor network could not be established."

    cv = r[1]+" "+r[5]

    if(cv!=version):
        return f"Update found for client !!!\n\nYou can download it here {program}"
    
    return"No updates found !!!"

print(update(version))

path = Rooms(True)
if not path:
    path=""

#AES key load
try:
    if path!="private":
        with open(path,"rb") as f:
            password = getpass.getpass("Enter the key password:").encode()
            key_ciphertext = f.read()
            dec = AES_cryptography.decryptor(password,sha1(password).digest())
            passwd = dec.decrypt(key_ciphertext)

            while not passwd.endswith(b"unencrypted"):
                print("Wrong password.\n")
                password = getpass.getpass("Enter the key password:").encode()
                dec = AES_cryptography.decryptor(password,sha1(password).digest())
                passwd = passwd = dec.decrypt(key_ciphertext)
        
            passwd = passwd[:len("unencrypted")*(-1)]
            IV = sha256(sha256(passwd).digest()).digest()
            f.close()

        password = "A"*len(password)*2
        del password
        del dec
        print("Key decrypted.")
except FileNotFoundError:
    print("Key file did not found.\nYou can load it using the key_loader or generate it using the key_generator.")
    exit()

#Helper to stop the threads
global dead
dead = False

#on send_msg() it adds randomly one character in the start and at the end of the message. This way if you send the same message
#it wont have the same bytes when it is encrypted

chars = ascii_letters+digits+"~`!@#$%^&*()_+-={}[]\\:;'\"<>,./?"


global spamm
spamm = time.time()

chat_plain_keyword = "1bn&jbsdo(F"

if path!="private":

    chat_room_key = sha512(sha512(passwd).digest()).hexdigest()


#Helper to run the start method of the threads once !
run = False

server_manager = loadServers.serversManagment()
server_manager.load("data/servers/servers.txt")

available_servers = server_manager.digest()
try:
    available_servers.remove("")
except:pass

link = servers.serverManager(available_servers)
port = 4488

for i in available_servers:
    if i not in server_manager.digest():
        server_manager.add(i)

for i in server_manager.digest():
    if i not in available_servers:
        server_manager.remove(i)

if link=="":exit()

print(f"Trying to connect to {link}")
#Checks if the server is online.
while True:
    try:
        testsock = torSocks(link,port)
        testsock.connect()
        testsock.setTimeout(3)
        testsock.send("online".encode())
        if testsock.recv(5) == b"True":
            testsock.close()
            break
        print("Failed to connect or the server is full. Trying again.")
    except KeyboardInterrupt:
        exit()
    except:
        print("Failed to connect or the server is full. Trying again.")
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        exit()

if path=="private":
    print("receiving key")
    try:
        keysock = torSocks(link,port)
        keysock.connect()
        keysock.setTimeout(3)
        keysock.send("private".encode())
        passwd = keysock.recv(32)
        keysock.close()
        if passwd==b"0":
            print("This server is not private.")
            exit()
        print("Key received !")
    except:
        print("Failed to receiv key")
        exit()
    
    IV = sha256(sha256(passwd).digest()).digest()
    chat_room_key = sha512(sha512(passwd).digest()).hexdigest()




#login screen

def reg(*event):
    register(link)
def login(*event):
    username = eusername.get()
    password = sha256((link+epassword.get()).encode()).digest()
    if not (2<=len(username.encode())<=10):
        tk_messagebox.showerror(title="Error",message="Wrong username or password")
        return
    
    try:
        global client_socket
        client_socket = torSocks(link,port)
        client_socket.connect()
        client_socket.send(b"login:%s:%s:%s" % (username.encode(),password, chat_room_key.encode()))
        ans = client_socket.recv(6).decode().strip()
        if "True" in ans:
            login_screen.destroy()
            return
        tk_messagebox.showerror(title="Error",message="Wrong username or password")
    except UnicodeEncodeError:
        tk_messagebox.showerror(title="Error",message="Try ascii chars")
    except UnicodeDecodeError:
        tk_messagebox.showerror(title="Error",message="This server is modified")
    except:
        tk_messagebox.showerror(title="Error",message="Server did not respond, try again.")

login_screen = tk.Tk()

login_screen.bind("<Return>",login)
login_screen.protocol("WM_DELETE_WINDOW",exit)
login_screen.title("login")
login_screen.resizable(0,0)

center_window(login_screen,205,200)
luname = tk_Label(login_screen, text="Username:") 
eusername = tk_Entry(login_screen,width=15)
lpass = tk_Label(login_screen,text="Password:")
epassword = tk_Entry(login_screen,width=15, show="*")
lbutton = tk_Button(login_screen, text="login", height=4,width=10, command=login)
regl = tk_Label(login_screen, cursor="hand2", text="Click here to register")
regl.bind("<Button-1>",reg)


luname.grid(row=0,column=0)
eusername.grid(row=0,column=1)
lpass.grid(row=1,column=0)
epassword.grid(row=1,column=1)
lbutton.place(relx=0.25,rely=0.3)
regl.place(rely=0.9)

login_screen.mainloop()

#functions

def send_msg(*event):
    global spamm

    if round(time.time()-spamm, 2) < 2:
        show_message("#Wait 2 seconds before you send another message")
        return

    if len(input_box.get()) == 0:return
    if len(input_box.get().encode())+2 > 80:
        show_message("#This message is too big")
        return
    encrypt = AES_cryptography.encryptor(passwd,IV)
    try:
        message = (choice(chars)+input_box.get()+choice(chars)).encode()
        ciphertext = encrypt.encrypt(message)
        tries = 0
        while tries < 100 and input_box.get().encode() in ciphertext:
            message = (choice(chars)+input_box.get()+choice(chars)).encode()
            encrypt = AES_cryptography.encryptor(passwd,IV)
            ciphertext = encrypt.encrypt(message)
            tries+=1
        
        if input_box.get().encode() in ciphertext:
            show_message("#There was a problem on sending this message.")
            return
        leng = len(input_box.get())
        input_box.delete(0,leng)
        try:
            client_socket.send(ciphertext)
            spamm = time.time()
            ciphertext = "A"*(len(ciphertext)*2)
        except:
            show_message("#Failed to send.")
    except UnicodeEncodeError:
        show_message("#Try ascii characters")

def recv_message():
    global dead
    while not dead:
        message = ""
        try:
            client_socket.setTimeout(0.2)
            message = client_socket.recv(100)
            if len(message)>1 and message.split(b":")[0] == b"Server":
                try:
                    message = message.decode()
                except UnicodeDecodeError:
                    message = "#Could not recv message from server"
            elif len(message)>1:
                decrypt = AES_cryptography.decryptor(passwd,IV)
                message = message.split(b":")
                try:
                    message = [message[0]+b": ",decrypt.decrypt(b":".join(message[1:]))[1:-1]]
                    try:
                        message = b''.join(message).decode()
                    except UnicodeDecodeError:
                        message = ""
                except:
                    message = ""
        except:
            pass
        
        if(len(message)>0):
            show_message(message)

def on_closing():
    global dead
    dead = True
    try:
        client_socket.send("COMMAND:D".encode())
        client_socket.close()
    except:
        print("Server closed or kicked you !")
    root.destroy()
    print("You have disconnected. Please wait !")

def donate():
    path = getcwd()+"/data/html/index.html"
    webbrowser.open(path)

def show_message(ms):
    msg_show.config(state="normal")
    msg_show.yview_pickplace("end")
    msg_show.insert("end",ms+"\n")
    msg_show.config(state="disable")

def show_participants(event):
    global spamm
    if round(time.time()-spamm, 2) < 2:
        show_message("#Wait 2 seconds before you send another message\n")
        return
    else:
        spamm=time.time()
    client_socket.send("COMMAND:S".encode())

global client_socket

#threads
thread_recv_message = threading.Thread(target=recv_message)

#Graphicks of main window

root = tk.Tk()

#Tk window Geometry
center_window(root,400,510)

#configuring window

root.title("SPC-Chat")
root.protocol("WM_DELETE_WINDOW",on_closing)
root.bind("<Return>",send_msg)
root.bind("<Tab>", show_participants)
root.resizable(0,0)

#Objects in tk window

chat_frame = tk_Frame(root, highlightbackground="black", highlightthickness=1)

#chat_frame

msg_show = tk_Text(chat_frame, state = "disabled", width = 49, height = 20, cursor="arrow")
text = tk_Label(chat_frame,text="Your messages are encrypted with your key.\nOnly people who have this key can read\nyour messages")
input_box = tk_Entry(chat_frame,width=40)
send_button = tk_Button(chat_frame, text="Send", cursor="hand2", command=send_msg)
donate_label = tk_Label(chat_frame,text="Small amounts can bring bigger impacts.")
donate_button = tk_Button(chat_frame,text="Donate", command = donate)


chat_frame.place(relx=0, relwidth=1, relheight=1)
msg_show.grid(row=0,column=0)
text.grid(row=1,column=0)
input_box.grid(row=2,column=0)
send_button.grid(row=3,column=0)
donate_label.grid(row=4,column=0)
donate_button.grid(row=5,column=0)

if(not run):
    thread_recv_message.start()
    run = True

root.mainloop()


passwd=password=IV=msg_show=client_socket = "A"*2048

del passwd, password , IV , msg_show , client_socket