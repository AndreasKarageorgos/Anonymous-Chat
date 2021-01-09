#coded by Andreas Karageorgos
#GitHub: https://github.com/AndreasKarageorgos/

import tkinter as tk
from tkinter import Entry as tk_Entry , Text as tk_Text,Label as tk_Label
from tkinter import Button as tk_Button, messagebox as tk_messagebox, Frame as tk_Frame, PhotoImage
from data.libraries import AES_cryptography, servers, loadServers
from data.libraries.register import register
from data.libraries.torSocks import torSocks
from data.libraries.rooms import Rooms
from data.libraries.askpass import askpass 
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
from platform import uname

def main():

    def center_window(window,width_of_window,height_of_window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))


    global sl
    if uname()[0].lower().startswith("win"):
        sl = "\\"
    else:
        sl = "/"

    #Checks for updates


    version = "version 1.11.1"

    def update(version):

        prox = {
            "https": "socks5://127.0.0.1:9050"
        }  

        program = "https://github.com/AndreasKarageorgos/SPC-Chat/ \n"
        
        try:
            r = requests.get("https://raw.githubusercontent.com/AndreasKarageorgos/SPC-Chat/master/VERSIONS", proxies = prox).text.split()
        except:
            return "Failed"

        cv = r[1]+" "+r[5]

        if(cv!=version):
            return f"Update found for client !!!\n\nYou can download it here {program}"
        
        return"No updates found !!!"

    utemp = update(version)

    if utemp == "Failed":
        print("Failed to connect to Tor")
        return
    else:
        print(utemp)
    
    del utemp

    path = Rooms(True)
    if not path:
        path=""

    #AES key load
    try:
        with open(path,"rb") as f:
            try:
                password = askpass().encode()
            except AttributeError:
                return
            key_ciphertext = f.read()
            dec = AES_cryptography.decryptor(password,sha1(password).digest())
            passwd = dec.decrypt(key_ciphertext)
            try:
                while not passwd.endswith(b"unencrypted"):
                    if uname()[0].lower().startswith("win"):
                        tk_messagebox.showinfo(message="Wrong password !")
                    else:
                        print("Wrong password.\n")
                    password = askpass().encode()
                    dec = AES_cryptography.decryptor(password,sha1(password).digest())
                    passwd = dec.decrypt(key_ciphertext)
            except KeyboardInterrupt:
                return
            except AttributeError:
                return

            passwd = passwd[:len(b"unencrypted")*(-1)]
            
            if len(passwd)!=48:
                print("This key is no longer supported.\nPlease generate a new one.")
                return

            IV = passwd[32:48]
            passwd = passwd[:32]
            f.close()

            password = "A"*len(password)*2
            del password
            del dec
            print("Key decrypted.")
    except FileNotFoundError:
        return

    #Helper to stop the threads
    global dead
    dead = False

    #on send_msg() it adds randomly one character in the start and at the end of the message. This way if you send the same message
    #it wont have the same bytes when it is encrypted

    chars = ascii_letters+digits+"~`!@#$%^&*()_+-={}[]\\:;'\"<>,./?"


    global spamm
    spamm = time.time()

    #chat_plain_keyword = "1bn&jbsdo(F"
    chat_room_key = sha512(passwd).digest()


    #Helper to run the start method of the threads once !
    run = False

    server_manager = loadServers.serversManagment()
    server_manager.load(f"data{sl}servers{sl}servers.txt")

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

    if link=="":return

    print(f"Connecting to {link}")
    #Checks if the server is online.
    while True:
        try:
            testsock = torSocks(link,port)
            try:
                testsock.connect()
            except OSError:
                print("Server closed.")
                return
            testsock.setTimeout(3)
            testsock.send("online".encode())
            if testsock.recv(5) == b"True":
                print("Connected !")
                testsock.close()
                break
            testsock.close()
            print("Failed to connect or the server is full. Trying again in 10 seconds.")
        except KeyboardInterrupt:
            return
        except:
            print("Failed to connect or the server is full. Trying again in 10 seconds.")
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            return

    



    #login screen

    def reg(*event):
        register(link)
    def login(*event):
        username = eusername.get()
        password = sha256((link+epassword.get()).encode()).digest()
        if not (2<=len(username.encode())<=10):
            tk_messagebox.showerror(title="Error",message="Wrong username, password or whitelist on")
            return
        
        try:
            global client_socket
            client_socket = torSocks(link,port)
            client_socket.connect()
            client_socket.setTimeout(3)
            client_socket.send(b"lg%s%s%s" % (username.encode(),password, chat_room_key))
            ans = client_socket.recv(10).decode().strip()
            if len(ans.encode()) >=6:
                tk_messagebox.showerror(title="Error", message="Invalid answer from server.")
                return
            if "True" in ans:
                login_screen.destroy()
                return
            tk_messagebox.showerror(title="Error",message="Wrong username, password or whitelist on")
        except UnicodeEncodeError:
            tk_messagebox.showerror(title="Error",message="Try ascii chars")
        except UnicodeDecodeError:
            tk_messagebox.showerror(title="Error",message="Failed to decode the bytes from server.")
        except:
            tk_messagebox.showerror(title="Error",message="Server did not respond, try again.")

    global shu
    shu = False
    def shut():
        global shu
        shu = True
        login_screen.destroy()

    login_screen = tk.Tk()
    login_screen.bind("<Return>",login)
    login_screen.protocol("WM_DELETE_WINDOW",shut)
    login_screen.title("login")
    login_screen.resizable(0,0)
    img = PhotoImage(file=f"data{sl}logo{sl}logo.png")
    login_screen.tk.call('wm', 'iconphoto', login_screen._w, img)
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

    if shu:
        return

    #functions

    def send_msg(*event):
        global spamm

        if round(time.time()-spamm, 2) < 2.3:
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
                message = client_socket.recv(150)
                if len(message)>100:
                    message = ""
                    client_socket.close()
                    tk_messagebox.showwarning(title="Warning", message="Server tried to flood your connection.\nYou have been disconnected !")
                    return
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
                        message = "Can not decrypt the message"

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
            print("Connection lost")
        root.destroy()
        print("you have been disconnected from the server. Please wait !")

    def donate():
        ans = tk_messagebox.askquestion(title="warning !", message="You are going to\nwww.spcchat.com/donates\nDo you want to continue ?")
        if ans == "yes":
            webbrowser.open("https://www.spcchat.com/donates")

    def show_message(ms):
        msg_show.config(state="normal")
        msg_show.yview_pickplace("end")
        msg_show.insert("end",ms+"\n")
        msg_show.config(state="disable")

    def show_participants(event):
        global spamm
        if round(time.time()-spamm, 2) < 2.3:
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
    img = PhotoImage(file=f"data{sl}logo{sl}logo.png")
    root.tk.call('wm', 'iconphoto', root._w, img)

    #Objects in tk window

    chat_frame = tk_Frame(root, highlightbackground="black", highlightthickness=1)

    #chat_frame

    msg_show = tk_Text(chat_frame, state = "disabled", width = 49, height = 20, cursor="arrow")
    text = tk_Label(chat_frame,text="\nYour messages are encrypted !\n")
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

main()