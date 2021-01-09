import tkinter as tk
from tkinter import Label as tk_Label , Entry as tk_Entry , Button as tk_Button , messagebox as tk_messagebox, PhotoImage
import socks
from hashlib import sha256
from data.libraries.torSocks import torSocks

def center_window(window,width_of_window,height_of_window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

def register(link):

    def send(uname,passwd):
        try:
            socket = torSocks(link,4488)
            passwd =  sha256((link+passwd).encode()).digest()
            socket.send(b"rg%s%s" % (uname.encode(),passwd))
            try:
                socket.setTimeout(10)
                suc = socket.recv(5)
                if suc==b"True":
                    tk_messagebox.showinfo(title="Success !", message="successfully registered to server !")
                    reg.destroy()
                else:
                    tk_messagebox.showerror(title="Error", message="Username already exists or whitelist on.")
            except:
                tk_messagebox.showerror(title="Error", message="Server did not respond")
        except:
            tk_messagebox.showerror(title="Error", message="Server did not respond")


    def reg_to_server():
        
        uname = username_entry.get()
        password = password_entry.get()
        if len(uname.encode()) < 2 or len(uname.encode()) > 10 or len(password.encode())>100 or len(password.encode())<12:
            tk_messagebox.showerror(title="Error", message="Username 2 to 10 characters\nPassword 12 to 100 chars\n(Non ascii characters can count more than just 1 character)")
            return
        elif ":" in uname:
            tk_messagebox.showerror(title="Error", message="the character \":\" is not allowed")
            return
        send(uname,password)
    

    reg = tk.Tk()
    #window geormetry

    center_window(reg,170,100)

    #Configure window

    reg.title("Register")
    reg.resizable(0,0)
    
    #objects in window

    username_label = tk_Label(reg,text = "username:")
    username_entry = tk_Entry(reg,width = 10)

    password_label = tk_Label(reg,text = "password:")
    password_entry = tk_Entry(reg,width = 10, show="*")

    submit_button = tk_Button(reg, text = "register", command = reg_to_server)

    #possitioning objext in window
    username_label.grid(row = 0, column = 0)
    username_entry.grid(row = 0, column = 1)

    password_label.grid(row = 1, column = 0)
    password_entry.grid(row = 1, column = 1)

    submit_button.grid(row = 2, column = 0)


    reg.mainloop()