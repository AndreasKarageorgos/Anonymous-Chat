import tkinter as tk
from tkinter import Entry as tk_Entry
from tkinter import Button as tk_Button
from tkinter import Frame as tk_Frame, Listbox as tk_Listbox
from tkinter import Checkbutton as tk_Checkbutton, IntVar as tk_IntVar
from tkinter import messagebox as tk_messagebox
from os import walk



def Rooms():

    def center_window(window,width_of_window,height_of_window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))



    global path
    path = ""
    
    
    def private_server():
        if checkbox_var.get():
            rooms.config(state="disable")
            tk_messagebox.showwarning(title="Low security", message="This option it's not secure !\n\nIf you connect to a server with this option enabled the owner of the server or anyone that has access to the machine that hosts the server will be able to decrypt your messages.\n\nAlso other people with this option enabled they are going to be able to see your messages and send messages to you.\n\nIf you understand the risk and you want to continue press the select button with the option enabled.")
        else:
            rooms.config(state="normal")

    def on_closing():
        global path
        path = False
        root.destroy()

    
    def select():
        global path
        if not checkbox_var.get():
            anchor = rooms.get("anchor")
            if anchor!="":
                root.destroy()
                path =  keys[anchor]
        else:
            path = "private"
            root.destroy()

    keys = {}

    for r,_,files in walk("data/key"):
        for f in files:
            if f.endswith(".key"):
                keys.update({f[:len(".key")*(-1)]:r+"/"+f})

    root = tk.Tk()

    #Tk window Geometry
    center_window(root,300,450)

    #configuring window

    root.protocol("WM_DELETE_WINDOW",on_closing)
    root.title("rooms")
    root.resizable(0,0)

    #Objects in tk window

    listframe = tk_Frame(root, highlightbackground="black", highlightthickness=1)
    listframe.place(relx=0, relwidth=1, relheight=0.7)


    rooms = tk_Listbox(listframe)



    rooms.pack(fill="both",expand="yes")


    buttonsframe = tk_Frame(root, highlightbackground="black", highlightthickness=1)
    buttonsframe.place(relx=0, rely=0.7, relwidth=1,relheight=0.3)

    selectbutton = tk_Button(buttonsframe, text="select", height=4,width=10, command=select)
    checkbox_var = tk_IntVar()
    private_checkbox = tk_Checkbutton(buttonsframe, text="I will connect to a private server.", variable=checkbox_var, command=private_server)

    selectbutton.place(relx=0.333,rely=0.1)
    private_checkbox.place(relx=0.01,rely=0.8)

    for k in keys:
        rooms.insert("end", k)

    root.mainloop()
    return path