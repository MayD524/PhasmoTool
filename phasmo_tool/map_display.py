from tkinter import *

try:
    import PIL

except ImportError:
    from sys import executable
    from os import system
    system(f"{executable} -m pip install pillow")
    import PIL

def resize_image(image_path:str, name:str) -> None:
    basewidth = 1280
    img = PIL.Image.open(image_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
    if name == "Grafton Farmhouse":
        baseheight = 1080
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    
    img.save(image_path)
    
def displayMap(map_name:str, map_images:dict):
    win = Toplevel()
    win.title(f"C69 PhasmoTool : {map_name}")
    win.resizable(True, True)
    
    img_path = f"./images/maps/{map_images[map_name]}"
    resize_image(img_path, map_name)
    
    img = PhotoImage(file=img_path)
    
    
    canvas = Canvas(win, width=1280, height=1280)
    canvas.pack()
    canvas.create_image(1280/2, 1280/2,image=img)
    
    win.mainloop()