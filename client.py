#Coded by Andreas Karageorgos

import tkinter as tk
from tkinter import Entry as tk_Entry , Text as tk_Text,Label as tk_Label, Button as tk_Button
from data import AES_cryptography
from random import choice
from string import ascii_letters,digits
from data import checkForUpdates
import webbrowser
import socket
import socks
import threading
import time

#Checks for updates

print("Checking for updates...\n")

print(checkForUpdates.check()+"\n")



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

#on send_msg() it adds randomly one character in the start and at the end of the message. This way if you send the same message
#it wont have the same bytes when it is encrypted

chars = ascii_letters+digits+"~`!@#$%^&*()_+-={}[]\\:;'\"<>,./?"

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

#functions
def send_msg():
    global keyword

    if len(input_box.get()) == 0:return
    if len(input_box.get()+keyword)+2 > 80:
        msg_show.config(state="normal")
        msg_show.insert(tk.INSERT,"\n***This message is too big***\n")
        msg_show.config(state="disable")
        return
    encrypt = AES_cryptography.encryptor(passwd,IV)
    message = (choice(chars)+input_box.get()+keyword+choice(chars)).encode("ascii")
    ciphertext = encrypt.encrypt(message)
    print(ciphertext)
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
                    message = [message[0]+b":",decrypt.decrypt(b":".join(message[1:]))[1:-1]]
                    message = b''.join(message).decode("ascii")
                    if message.endswith(keyword) and (len(message)-len(keyword)) > 0:
                        message = message[:len(message)-len(keyword)]+"\n"
                    else:
                        message = ""
                except:
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

def donate():
    def paypal():webbrowser.open(f"https://paypal.me/AndreasKarageorgos/{paypal_amount.get()}")
    def BitCoin():webbrowser.open(f"https://www.blockchain.com/btc/payment_request?address=1DJqJtMGRzG12NZk1SJ5DnCfpeunTX1z1V&amount={bitcoin_ammount.get()}&message=Anonymous%20Chat%20donation%20!Thank%20you%20for%20your%20support%20!!!%20%3C3")

    x = 0

    master = tk.Tk()
    width_of_window = 200
    height_of_window = 100
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
        bitcoin_ammount.insert(0,"0.00198")
        x=1

    paypal_button.grid(row=0,column=0)
    paypal_amount.grid(row=0,column=1)
    pypal_payS.grid(row=0,column=2)
    
    bitcoin_button.grid(row=1,column=0)
    bitcoin_ammount.grid(row=1,column=1)
    bitcoin_payS.grid(row=1,column=2)
    
    master.mainloop()


#threads
thread_recv_message = threading.Thread(target=recv_message)

#Graphicks

root = tk.Tk()

width_of_window = 400
height_of_window = 510
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

root.title("Anonymous Chat !")
root.protocol("WM_DELETE_WINDOW",on_closing)

msg_show = tk_Text(root, state = "disabled", width = 49, height = 20, cursor="arrow")
text = tk_Label(root,text="Do not open links or send anything that\ncan trace back to you !")
input_box = tk_Entry(root,width=40)
send_button = tk_Button(root, text="Send", cursor="hand2", command=send_msg)
donate_label = tk_Label(root,text="You can help me to keep updating this project\nby donating. <3")
donate_button = tk_Button(root,text="Donate Options", command = donate)

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