from main_gui import phasmoToolGui
from tkinter import *
import C69_updater
import C69_common

try:
    import UPL

except ImportError:
    import sys, os
    print(chr(69))
    os.system(f"{sys.executable} ./auto_upl.py")
    os.system(f"{sys.executable} -m pip install psutil")
    import UPL

## update this per version (used in updater)
## Major.Minor.Part.Bug fix
__version__ = '0.2.8'

def boot_window():
    win = Tk()
    win.title("C69 PhasmoTool")
    win.resizable(False, False)
    canvas = Canvas(win, width=300, height=300)
    welcomeText = Label(win, text="Welcome to Char 69 Dev Team's, PhasmoTool!\nCheck the about section for more info")
    canvas.pack()
    welcomeText.pack()
    
    C69_common.resize_image("./images/icons/boot_img.png", 300, 300)
    img = PhotoImage(file="./images/icons/boot_img.png")
    canvas.create_image(150, 150, image=img)
     
    win.after(3500, lambda:win.destroy())  
    win.mainloop()
    
if __name__ == "__main__":
    config = UPL.Core.file_manager.getData_json("./json/conf.json")
    
    if config["allow_auto_update"]:
        need_update = C69_updater.check_update("phasmo_tool", __version__)
        
        if need_update[0]:
            if UPL.gui.confirm("C69 Phasmo Tool", f"Do you want to update to version {need_update[1]['version']}", ["Yes", "No"]) == "Yes":
                C69_updater.update_program("phasmo_tool")
    
    if not config['debug_mode']:
        boot_window()
    else:
        print(chr(69))
        print(config)    
    phasmoToolGui(config)