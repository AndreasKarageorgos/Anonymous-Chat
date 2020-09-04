import tkinter as tk
from tkinter import Label as tk_Label , Entry as tk_Entry , Button as tk_Button , messagebox as tk_messagebox
import socks
try:
    from data.libraries.torSocks import torSocks
except:
    from torSocks import torSocks

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
            socket.connect()
            socket.send(f"register:{uname}:{passwd}".encode("ascii"))
            try:
                socket.setTimeout(10)
                suc = socket.recv(5)
                if suc==b"True":
                    tk_messagebox.showinfo(title="Success !", message="successfully registered to server !")
                    reg.destroy()
                else:
                    tk_messagebox.showerror(title="Error", message="Failed to register")
            except:
                tk_messagebox.showerror(title="Error", message="Failed to register")
        except:
            tk_messagebox.showerror(title="Error", message="Failed to register")


    def reg_to_server():
        
        uname = username_entry.get()
        password = password_entry.get()
        if len(uname) < 2 or len(uname) > 10 or len(password)>100 or len(password)<12:
            tk_messagebox.showerror(title="Error", message="Username 2 to 10 chars\nPassword 12 to 100 chars\n(Only ascii characters are accepted !)")
            return
        elif ":" in uname or ":" in password:
            tk_messagebox.showerror(title="Error", message="The character ':' is not allowed.")
            return
        send(uname,password)
    

    reg = tk.Tk()
    #window geormetry

    center_window(reg,170,100)

    #Configure window

    reg.title("Register")
    reg.resizable(0,0)
    tk_messagebox.showwarning(title="warning", message="Make sure that you will not use your real credentials.\n")
    #objects in window

    username_label = tk_Label(reg,text = "username:")
    username_entry = tk_Entry(reg,width = 10)

    password_label = tk_Label(reg,text = "password:")
    password_entry = tk_Entry(reg,width = 10)

    submit_button = tk_Button(reg, text = "register", command = reg_to_server)

    #possitioning objext in window
    username_label.grid(row = 0, column = 0)
    username_entry.grid(row = 0, column = 1)

    password_label.grid(row = 1, column = 0)
    password_entry.grid(row = 1, column = 1)

    submit_button.grid(row = 2, column = 0)


    reg.mainloop()