import tkinter as tk
import threading
from os import remove as os_remove
from tkinter import Entry as tk_Entry
from tkinter import Button as tk_Button
from tkinter import Frame as tk_Frame, Listbox as tk_Listbox
from tkinter import Checkbutton as tk_Checkbutton, IntVar as tk_IntVar
from tkinter import messagebox as tk_messagebox , PhotoImage
from os import walk
from data.libraries.key_generator import key_generator




def Rooms(pr):

    def kl(t=True):
        for r,_,files in walk("data/key"):
            for f in files:
                if f.endswith(".key") :
                    keys.update({f[:len(".key")*(-1)]:r+"/"+f})
        if t:
            rooms.delete(0,"end")
            for k in keys:
                rooms.insert("end", k)


    def keygen():
        threading.Thread(target=key_generator).start()

    def center_window(window,width_of_window,height_of_window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

    def delete():
        global path
        global keys
        select(False)
        if path!= None:
            ans = tk_messagebox.askquestion(title="delete", message=f"Are you sure that you want to delete {rooms.get('anchor')}?")
            if ans=="yes":
                with open(path, "wb") as f:
                    f.write("A".encode()*100)
                    f.close()
                os_remove(path)
                keys = {}
                path = None
                kl()
        


    global path
    path = None
    
    
    def refreshme():
        kl()
        tk_messagebox.showinfo(title="R", message="Refreshed")

    def on_closing():
        global path
        path = False
        root.destroy()

    
    def select(cl=True):
        global path
        try:
            anchor = rooms.get("anchor")
            if anchor!="":
                path =  keys[anchor]
                if cl:
                    root.destroy()
        except:
            path = None

    global keys
    keys = {}
    kl(False)
    root = tk.Tk()

    #Tk window Geometry
    center_window(root,300,450)

    #configuring window

    root.protocol("WM_DELETE_WINDOW",on_closing)
    root.title("rooms")
    root.resizable(0,0)
    img = PhotoImage(file="data/logo/logo.png")
    root.tk.call('wm', 'iconphoto', root._w, img)

    #Objects in tk window

    listframe = tk_Frame(root, highlightbackground="black", highlightthickness=1)
    listframe.place(relx=0, relwidth=1, relheight=0.7)


    rooms = tk_Listbox(listframe)



    rooms.pack(fill="both",expand="yes")


    buttonsframe = tk_Frame(root, highlightbackground="black", highlightthickness=1)
    buttonsframe.place(relx=0, rely=0.7, relwidth=1,relheight=0.3)

    selectbutton = tk_Button(buttonsframe, text="select", height=1,width=10, command=select)
    generatebutton = tk_Button(buttonsframe, text="create room", height=1,width=10, command=keygen)
    deletebutton = tk_Button(buttonsframe, text="delete", height=1,width=10, command=delete)
    checkbox_var = tk_IntVar()
    refresh = tk_Button(buttonsframe, width=2, text="R" , command=refreshme)

    selectbutton.place(relx=0.333,rely=0.1)
    if pr:
        refresh.place(relx=0.01,rely=0.75)
        generatebutton.place(relx=0.333, rely=0.35)
        deletebutton.place(relx=0.333, rely = 0.6)

    for k in keys:
        rooms.insert("end", k)

    root.mainloop()
    return path