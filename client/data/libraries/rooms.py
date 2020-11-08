import tkinter as tk
from tkinter import Entry as tk_Entry
from tkinter import Button as tk_Button, Frame as tk_Frame, Listbox as tk_Listbox
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
    
    
    def on_closing():
        global path
        path = False
        root.destroy()

    
    def select():
        global path

        anchor = rooms.get("anchor")
        if anchor!="":
            root.destroy()
            path =  keys[anchor]

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

    selectbutton.place(relx=0.333,rely=0.2)

    for k in keys:
        rooms.insert("end", k)

    root.mainloop()
    return path