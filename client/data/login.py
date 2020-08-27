from hashlib import sha512
import tkinter as tk
import socks
from tkinter import Label as tk_Label , Entry as tk_Entry , Button as tk_Button , messagebox as tk_messagebox

def center_window(window,width_of_window,height_of_window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))



def login(socket,link):

    def login_to_server():
        try:
            uname = username_entry.get()
            passwd = password_entry.get()
            socket.connect((link,4488))
            socket.send(f"login:{uname}:{passwd}".encode("ascii"))
            socket.settimeout(10)
            resp = bool(socket.recv(6).decode("ascii").strip())
            if not resp:
                tk_messagebox.showerror(title="Error",message="Failed to log in")
                socket.close()
            helper()
        except UnicodeEncodeError:
            tk_messagebox.showerror(title="Error", message="Only ascii characters are allowed.")
        except:
            tk_messagebox.showerror(title="Error", message="Failed to login")

    global x
    x = 0
    def helper():
        global x
        x = 1

    login = tk.Tk()
    #window geormetry

    center_window(login,170,100)

    #Configure window

    login.title("login")
    login.resizable(0,0)
    tk_messagebox.showwarning(title="warning", message="Do not use usernames and passwords that you use on your social media or enything that can be linked back to you.\nAlso use different usernames and passwords in different servers.")
    #objects in window

    username_label = tk_Label(login,text = "username:")
    username_entry = tk_Entry(login,width = 10)

    password_label = tk_Label(login,text = "password:")
    password_entry = tk_Entry(login,width = 10)


    submit_button = tk_Button(login, text = "login", command = login_to_server)



    #possitioning objext in window
    username_label.grid(row = 0, column = 0)
    username_entry.grid(row = 0, column = 1)

    password_label.grid(row = 1, column = 0)
    password_entry.grid(row = 1, column = 1)

    submit_button.grid(row = 2, column = 0)

    if x==1:
        login.destroy()
        return socket

    login.mainloop()