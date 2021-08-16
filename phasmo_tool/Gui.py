from main_gui import phasmoToolGui
from tkinter import ttk
from tkinter import *

def boot_window():
    win = Tk()
    win.title("C69 PhasmoTool")
    win.resizable(False, False)
    canvas = Canvas(win, width=300, height=300)
    canvas.pack()
    img = PhotoImage(file="icon.png")
    canvas.create_image(150, 150, image=img)
    
    win.after(5000, lambda:win.destroy())
    
    win.mainloop()
    
if __name__ == "__main__":
    boot_window()
    phasmoToolGui()