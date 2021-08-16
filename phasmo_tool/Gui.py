from sys import version
from main_gui import phasmoToolGui
from tkinter import *
import C69_updater

## update this per version (used in updater)
__version__ = '0.2.3'

def boot_window():
    win = Tk()
    win.title("C69 PhasmoTool")
    win.resizable(False, False)
    canvas = Canvas(win, width=300, height=300)
    canvas.pack()
    img = PhotoImage(file="./images/icons/icon.png")
    canvas.create_image(150, 150, image=img)
    
    win.after(5000, lambda:win.destroy())
    
    win.mainloop()
    
if __name__ == "__main__":
    need_update = C69_updater.check_update("phasmo_tool", __version__)
    print(need_update)
    
    if need_update[0]:
        C69_updater.update_program("phasmo_tool")
    
    boot_window()
    phasmoToolGui()