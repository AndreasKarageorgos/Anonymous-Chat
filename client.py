#Coded by Andreas Karageorgos

import tkinter as tk
from tkinter import Entry as tk_Entry , Text as tk_Text,Label as tk_Label, Button as tk_Button ,Scrollbar as tk_Scrollbar
from data import AES_cryptography
import socket
import socks
import threading
import time

#AES key load
try:
    with open("data/key/AES.key","r") as f:
        passwd = f.read().strip().encode("ascii")  
        f.close()

    with open("data/key/IV.key","r") as f:
        IV = f.read().strip().encode("ascii")
        f.close()
except FileNotFoundError:
    print("Did not find key files. Please use the key_generator.py")
    exit()

#Helper to stop the threads
global dead
dead = False

#Key word is helping to decrypt the messages of the people that you want to talk

global keyword
keyword = input("Enter a key word: ").strip() or "nokey" 

#Helper to run the start method of the threads once !
run = False


link = input("Onion link: ")
while not link.endswith(".onion"):
    print("Please enter an onion link !\n")
    link = input("Onion Link: ")

port = 4488


while True:
    try:
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
        client_socket = socks.socksocket()
        client_socket.settimeout(10)
        client_socket.connect((link,port))
        break
    except KeyboardInterrupt:
        exit()
    except:
        print("Can not connect to server !\nTrying again in 5 seconds")
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            exit()
    
#Donate link
print("You can help me to keep updating this project by donating to my paypal: https://paypal.me/AndreasKarageorgos/")

#functions
def send_msg():
    global keyword

    if len(input_box.get()) == 0:return
    if len(input_box.get()+keyword) > 80:
        msg_show.config(state="normal")
        msg_show.insert(tk.INSERT,"\n***This message is too big***\n")
        msg_show.config(state="disable")
        return
    encrypt = AES_cryptography.encryptor(passwd,IV)
    message = (input_box.get()+keyword).encode("ascii")
    ciphertext = encrypt.encrypt(message)
    leng = len(input_box.get())
    input_box.delete(0,leng)
    try:
        client_socket.send(ciphertext)
    except:
        msg_show.config(state="normal")
        msg_show.insert(tk.INSERT,"\n***Message did not send***\n")
        msg_show.config(state="disable")

def recv_message():
    global dead
    global keyword
    while not dead:
        message = ""
        try:
            message = client_socket.recv(1024)
            if len(message)>1 and message.split(b":")[0] == b"Server":
                message = message.decode("ascii") 
            elif len(message)>1:
                decrypt = AES_cryptography.decryptor(passwd,IV)
                message = message.split(b":")
                try:
                    message = [message[0]+b":",decrypt.decrypt(b":".join(message[1:]))]
                    message = b''.join(message).decode("ascii")
                    if message.endswith(keyword) and (len(message)-len(keyword)) > 0:
                        message = message[0:len(message)-len(keyword)]+"\n"
                    else:
                        message = ""
                except:
                    print("Error")
                    message = ""
        except:
            pass
        
        if(len(message)>0):
            msg_show.config(state="normal")
            msg_show.insert(tk.INSERT,message)
            msg_show.yview_pickplace("end")
            msg_show.config(state="disable")

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

#threads
thread_recv_message = threading.Thread(target=recv_message)

#Graphicks

root = tk.Tk()

width_of_window = 400
height_of_window = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

root.title("Anonymous Chat ! Alpha 0.1 V")
root.protocol("WM_DELETE_WINDOW",on_closing)

msg_show = tk_Text(root, state = "disabled", width = 49, height = 20)
text = tk_Label(root,text="Do not open links or send anything that\ncan trace back to you !")
input_box = tk_Entry(root,width=40)
send_button = tk_Button(root,text="Send",command=send_msg)
donate = tk_Label(root,text="You can help me to keep updating this project\nby donating to my paypal\nhttps://paypal.me/AndreasKarageorgos/")


msg_show.grid(row=0,column=0)
text.grid(row=1,column=0)
input_box.grid(row=2,column=0)
send_button.grid(row=3,column=0)
donate.grid(row=4,column=0)

if(not run):
    thread_recv_message.start()
    run = True

root.mainloop()