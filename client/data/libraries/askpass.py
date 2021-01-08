from tkinter import Tk, PhotoImage, Entry, Button
from platform import uname



def askpass(sh=False):
    
    global p
    p = None

    if uname()[0].lower().startswith("win"):
        sl = "\\"
    else:
        sl = "/"

    def done(*event):
        global p
        if password.get() != "":
            p = password.get()
            root.destroy()

    def on_closing():
        root.destroy()

    def center_window(window,width_of_window,height_of_window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

    root = Tk()
    center_window(root,200,100)
    if sh:
        root.title("name")
    else:
        root.title("password")
    try:
        img = PhotoImage(file=f"data{sl}logo{sl}logo.png")
        root.tk.call('wm', 'iconphoto', root._w, img)
    except:pass
        
    root.resizable(0,0)
    root.bind("<Return>",done)
    root.protocol("WM_DELETE_WINDOW",on_closing)
    
    if sh:
        password = Entry(root, width="15")
    else:
        password = Entry(root, width="15", show="*")

    button = Button(root, text="Enter", command=done)

    password.pack(pady=10)
    button.pack()

    root.mainloop()

    return p