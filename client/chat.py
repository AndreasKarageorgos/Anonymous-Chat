#coded by Andreas Karageorgos
#GitHub: https://github.com/AndreasKarageorgos/

import tkinter as tk
from tkinter import Entry as tk_Entry , Text as tk_Text,Label as tk_Label, Button as tk_Button, messagebox as tk_messagebox
from data.libraries import AES_cryptography, servers, loadServers
from data.libraries.register import register
from data.libraries.torSocks import torSocks
from random import choice
from string import ascii_letters,digits
from hashlib import sha256,sha512,sha1
import requests
import webbrowser
import socks
import threading
import time
import getpass

#Checks for updates


version = "Beta 1.4"

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


#AES key load
try:
    with open("data/key/Key.key","rb") as f:
        password = getpass.getpass("Enter the key password:").encode("ascii")
        key_ciphertext = f.read()
        dec = AES_cryptography.decryptor(password,sha1(password).digest())
        passwd = dec.decrypt(key_ciphertext)

        while not passwd.endswith(b"unencrypted"):
            print("Wrong password.\n")
            password = getpass.getpass("Enter the key password:").encode("ascii")
            dec = AES_cryptography.decryptor(password,sha1(password).digest())
            passwd = passwd = dec.decrypt(key_ciphertext)
       
        passwd = passwd[:len("unencrypted")*(-1)]
        IV = passwd[:16]
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

#Key word is helping the program to know that it decrypted the message.

global keyword
keyword = "D$o(n"

chat_plain_keyword = "*fgnHePofnq3*dhvH1)(dkf^"

temp_pass = sha256(passwd[:16]).digest()
temp_iv = temp_pass[:16]

chat_room_key = sha512(AES_cryptography.encryptor(temp_pass,temp_iv).encrypt(chat_plain_keyword.encode("ascii"))).hexdigest()

del temp_pass
del temp_iv

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
        testsock.send("online".encode("ascii"))
        if testsock.recv(5) == b"True":
            testsock.close()
            break
        print("Failed to connect. Trying again.")
    except KeyboardInterrupt:
        exit()
    except:
        print("Failed to connect. Trying again.")
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        exit()


ask = input("Press Enter to login or type 'R' to register: ").lower().strip()

while not(ask == "r" or ask==""):
    ask = input("Press Enter to login or type 'R' to register: ").lower().strip()

if ask=="r":
    register(link)



while True:
    try:
        uname = input("Username: ")
        password = getpass.getpass("Password: ")
        while not (2<=len(uname)<=10 and 12<=len(password)<=100):
            print("Wrong username or password\n")
            uname = input("Username: ")
            password = getpass.getpass("Password: ")
        client_socket = torSocks(link,port)
        client_socket.connect()
        client_socket.setTimeout(10)
        password = sha256((link+password).encode("ascii")).digest()
        client_socket.send(b"login:%s:%s:%s" % (uname.encode("ascii"),password, chat_room_key.encode("ascii")))
        ans = client_socket.recv(6).decode("ascii").strip()
        if "True" in ans:
            break
        print("Wrong username or password.\n")
    except KeyboardInterrupt:
        exit()
    except UnicodeEncodeError:
        print("Only ascii chars")
    except UnicodeDecodeError:
        print("This server is modified, you may not be able to send or recv any data. ")
    except:
        print("Server did not respond")
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            exit()

#functions

def send_msg(*event):
    global keyword
    if len(input_box.get()) == 0:return
    if len(input_box.get()+keyword)+2 > 80:
        show_message("***This message is too big***")
        return
    encrypt = AES_cryptography.encryptor(passwd,IV)
    try:
        message = (choice(chars)+input_box.get()+keyword+choice(chars)).encode("ascii")
        ciphertext = encrypt.encrypt(message)
        if keyword.encode("ascii") in ciphertext:
            show_message("***This message is not encrypted***")
            return
        leng = len(input_box.get())
        input_box.delete(0,leng)
        try:
            client_socket.send(ciphertext)
        except:
            show_message("***Failed to send the message***")
    except UnicodeEncodeError:
        show_message("***Ascii characters only***")

def recv_message():
    global dead
    global keyword
    while not dead:
        message = ""
        try:
            client_socket.setTimeout(0.2)
            message = client_socket.recv(100)
            if len(message)>1 and message.split(b":")[0] == b"Server":
                try:
                    message = message.decode("ascii")
                except UnicodeDecodeError:
                    message = ""
            elif len(message)>1:
                decrypt = AES_cryptography.decryptor(passwd,IV)
                message = message.split(b":")
                try:
                    message = [message[0]+b": ",decrypt.decrypt(b":".join(message[1:]))[1:-1]]
                    try:
                        message = b''.join(message).decode("ascii")
                        if message.endswith(keyword) and (len(message)-len(keyword)) > 0:
                            message = message[:len(message)-len(keyword)]
                        else:
                            message = ""
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
        client_socket.send("COMMAND:D".encode("ascii"))
        client_socket.close()
    except BrokenPipeError:
        print("Server closed or kicked you !")
    except:
        pass
    root.destroy()
    print("You have disconnected. Please wait !")

def donate():
    def paypal():webbrowser.open(f"https://paypal.me/AndreasKarageorgos/{paypal_amount.get()}")
    def BitCoin():webbrowser.open(f"https://www.blockchain.com/btc/payment_request?address=1DJqJtMGRzG12NZk1SJ5DnCfpeunTX1z1V&amount={bitcoin_ammount.get()}&message=Thank%20you%20for%20your%20support%20!!!%20%3C3")

    tk_messagebox.showwarning(title="Warning !",message="The buttons will promt you to the equivalent site.\n\nAfter you select your amount and click the the equivalent button it will\nStart your default browser.\n\nThat means that it can run outside of the Tor network.\n\nThe sites are from paypal and blockchain.com")
    
    x = 0

    master = tk.Tk()
    width_of_window = 200
    height_of_window = 70
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    master.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
    master.title("Donates")

    paypal_button = tk_Button(master,text = "paypal", command=paypal)
    paypal_amount = tk_Entry(master, width = 10)
    pypal_payS = tk.Label(master, text="‎€")
    
    bitcoin_button = tk_Button(master, text = "BitCoin", command=BitCoin)
    bitcoin_ammount = tk_Entry(master, width = 10)
    bitcoin_payS = tk_Label(master, text="₿")

    if x==0:
        paypal_amount.insert(0,"20")
        bitcoin_ammount.insert(0,"0.00223")
        x=1

    paypal_button.grid(row=0,column=0)
    paypal_amount.grid(row=0,column=1)
    pypal_payS.grid(row=0,column=2)
    
    bitcoin_button.grid(row=1,column=0)
    bitcoin_ammount.grid(row=1,column=1)
    bitcoin_payS.grid(row=1,column=2)
    
    master.mainloop()

def show_message(ms):
    msg_show.config(state="normal")
    msg_show.yview_pickplace("end")
    msg_show.insert("end",ms+"\n")
    msg_show.config(state="disable")

def show_participants(event):
    client_socket.send("COMMAND:S".encode("ascii"))

def center_window(window,width_of_window,height_of_window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))


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

msg_show = tk_Text(root, state = "disabled", width = 49, height = 20, cursor="arrow")
text = tk_Label(root,text="Do not open links or send anything that\ncan trace back to you !")
input_box = tk_Entry(root,width=40)
send_button = tk_Button(root, text="Send", cursor="hand2", command=send_msg)
donate_label = tk_Label(root,text="You can help me to keep updating this project\nby donating. <3")
donate_button = tk_Button(root,text="Donate Options", command = donate)

#Possitioning objects in window

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