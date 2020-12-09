import tkinter as tk
from tkinter import Listbox as tk_Listbox, Button as tk_Button , messagebox as tk_messagebox, Entry as tk_Entry, PhotoImage




def serverManager(lista):

    def center_window(window,width_of_window,height_of_window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
    
    def select():
        global link
        link = listBox.get("anchor")
        if link!="":
            root.destroy()

    def delete():
        if listBox.get("anchor")!="":
            lista.remove(listBox.get("anchor"))
            listBox.delete("anchor")

    def add():

        def confirm():
            l = Entry.get().strip()
            if l.endswith(".onion") and len(l)>len(".onion"):
                lista.append(l)
                listBox.insert("end",l)
            else:
                tk_messagebox.showerror(title="Invalid url", message="This is not a hidden service url")
            
            Entry.pack_forget()
            confirm_button.forget()
            add_button.pack(pady=5)

        confirm_button = tk_Button(root, text="Confirm", command=confirm)
        Entry = tk_Entry(root, width=20)

        add_button.pack_forget()
        confirm_button.pack(pady=5)
        Entry.pack()


    global link
    link = ""

    root = tk.Tk()
    center_window(root,500,360)
    root.title("Servers list")
    root.resizable(0,0)
    img = PhotoImage(file="data/logo/logo.png")
    root.tk.call('wm', 'iconphoto', root._w, img)


    listBox = tk_Listbox(root)
    select_button = tk_Button(root, text="Select", command=select)
    delete_button = tk_Button(root, text="Delete", command=delete)
    add_button = tk_Button(root, text="Add", command=add)



    listBox.pack(fill="both",expand="yes")
    select_button.pack(pady=5)
    delete_button.pack(pady=5)
    add_button.pack(pady=5)

    for i in lista:
        listBox.insert("end", i)

    root.mainloop()
    
    return (link)