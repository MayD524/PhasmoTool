from tkinter import *
import C69_common
import os
def lookup_tool(item:str, tools:dict) -> None:
    toolsWin = Toplevel()
    toolsWin.resizable(False, False)
    item = item.lower().title()
    item_dict = tools[item]
    
    toolsWin.title(f"C69 Phasmotool : {item}")
    pTool_icon = PhotoImage(file="./images/icons/icon.png")
    
    item_can = Canvas(toolsWin, width=250, height=250)
    desc_Text = Label(toolsWin, text=f"Description : {item_dict['Description']}")
    hiw_Text  = Label(toolsWin, text=f"How it works : {item_dict['How it works']}")
    mpr_Text  = Label(toolsWin, text=f"Max per round : {item_dict['Max per round']}")
    price_txt = Label(toolsWin, text=f"Price : {item_dict['Price']}")
    eviT_txt  = Label(toolsWin, text=f"Evidence Tool : {item_dict['Evidence_tool']}")

    item_can.pack()
    desc_Text.pack()
    hiw_Text.pack()
    mpr_Text.pack()
    price_txt.pack()
    eviT_txt.pack()

    ## path = f"./images/images/{item.lower()}.png"
    path = "./images/ghosts/tmp.png"
    C69_common.resize_image(path, 250, 250)

    img = PhotoImage(file=path)
    item_can.create_image(250//2, 250//2, image=img)
    
    ## icon and main loop
    toolsWin.iconphoto(False, pTool_icon)
    toolsWin.mainloop()
    

def lookup_ghost(ghost:str, ghosts:dict) -> None:
    ## create window & config
    ghostWin = Toplevel()
    ghostWin.resizable(False, False)
    ghost = ghost.lower().capitalize()
    ghostWin.title(f"C69 PhasmoTool : {ghost}")
    pTool_icon = PhotoImage(file="./images/icons/icon.png")
    
    ## create elements
    ghost_can     = Canvas(ghostWin, width=250, height=250)
    desc_Text     = Label(ghostWin, text=f"Description : {ghosts[ghost]['Description']}")
    Strenght_Text = Label(ghostWin, text=f"Strength : {ghosts[ghost]['Strength']}")
    Weakness_Text = Label(ghostWin, text=f"Weakness : {ghosts[ghost]['Weakness']}")
    Evidence_Text = Label(ghostWin, text=f"Evidence:\n{ghosts[ghost]['Evidence'][0]}\n{ghosts[ghost]['Evidence'][1]}\n{ghosts[ghost]['Evidence'][2]}")
    
    ## pack
    ghost_can.pack()
    desc_Text.pack()
    Strenght_Text.pack(ipadx=10, ipady=10)
    Weakness_Text.pack(ipadx=10, ipady=10)
    Evidence_Text.pack()
    
    ## image
    path = f"./images/ghosts/{ghost.lower()}.png"
    if not os.path.exists(path):
        path = "./images/ghosts/tmp.png"
    C69_common.resize_image(path, 250, 250)
    img = PhotoImage(file=path)
    ghost_can.create_image(250//2, 250//2, image=img)
    
    ## icon and main loop
    ghostWin.iconphoto(False, pTool_icon)
    ghostWin.mainloop()
    