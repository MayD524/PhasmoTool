from tkinter import *
import C69_common

def lookup_tool(tool_name:str) -> None:
    pass

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
    #path = f"./images/ghosts/{ghost.lower()}.png"
    path = "./images/ghosts/tmp.png"
    C69_common.resize_image(path, 250, 250)
    img = PhotoImage(file=path)
    ghost_can.create_image(250//2, 250//2, image=img)
    
    ## icon and main loop
    ghostWin.iconphoto(False, pTool_icon)
    ghostWin.mainloop()
    