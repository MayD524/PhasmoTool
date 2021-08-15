"""
    Authors: Cross/Ryan & Sweden/Jerk
    Date: 8/15/2021
"""
from core import phasmoTool
import tkinter 
import psutil
import UPL


ghosts = UPL.Core.file_manager.getData_json("ghosts.json")
phasTool = phasmoTool(ghosts)

def addBtnFunc() -> None:
    phasTool.add_evidence()
    ghost_list.delete(0, ghost_list.size())
    update_Ghosts()
    
def remBtnFunc() -> None:
    phasTool.rem_evidence()
    ghost_list.delete(0, ghost_list.size())
    update_Ghosts()
    if ghost_list.size() == 0:
        evidence_list.delete(0, evidence_list.size())
    
def lookBtnFunc() -> None:
    phasTool.lookup(UPL.gui.prompt("Ghost Index", "What ghost would you like to look up hunter?"))

def eviBtnFunc() -> None:
    if phasTool.current_round != []:
        msg = "\n\t".join(phasTool.current_round)
        UPL.gui.popup(msg=f"Current Evidence:\n\t{msg}", title="Current Evidence")
    
    else:
        UPL.gui.popup("Go find some evidence!", title="Current Evidence")

def clearBtnFunc() -> None:
    choice = UPL.gui.confirm("Clear", "Do you want this to clear the evidence?", ["Yes", "No"])
    if choice == "Yes":
        
        print(evidence_list.size())
        evidence_list.delete(0, evidence_list.size())
        ghost_list.delete(0, ghost_list.size())
        phasTool.current_round.clear()
        phasTool.current_guess()
        
    elif choice == "No":
        print("Not clearing")
    else:
        print(chr(69))

def update_Ghosts():
    index = 0
    for ghost in phasTool.possible:
        ghost_list.insert(index, ghost)
        index += 1

def update_Evidence(ghost:str) -> None:
    evidence_list.delete(0, evidence_list.size())
    index = 0
    for evidence in ghosts[ghost]["Evidence"]:
        evidence_list.insert(index, evidence)
        index += 1
        
def CurSelet(event):
    widget = event.widget
    selection=widget.curselection()
    picked = widget.get(selection[0])
    update_Evidence(picked)

def dontClick() -> None:
    phasTool.clicks += 1
    if phasTool.clicks == 199:
        UPL.gui.popup("Dont click one more time or i will close phasmo","Dont do it")
    
    elif phasTool.clicks == 200:
        for proc in psutil.process_iter():
            if "phasmo" in proc.name().lower():
                proc.kill()
                
if __name__ == "__main__":
    root = tkinter.Tk()  
    clicks = 0
    #stuff for scaling gui to make it nic
    tkinter.Grid.rowconfigure(root,0,weight=1)
    tkinter.Grid.columnconfigure(root,0,weight=1)
    tkinter.Grid.rowconfigure(root,1,weight=1)
    
    var = tkinter.StringVar()
    #button stuff
    addBtn = tkinter.Button(root, text="Add Evidence", command = addBtnFunc) 
    addBtn.grid(row=0,column=0,sticky="NSEW")
    remBtn = tkinter.Button(root, text="Remove Evidence", command = remBtnFunc) 
    remBtn.grid(row=0,column=1,sticky="NSEW")
    lookBtn = tkinter.Button(root, text="Lookup", command = lookBtnFunc) 
    lookBtn.grid(row=1,column=0,sticky="NSEW")
    clrBtn = tkinter.Button(root, text="Clear", command = clearBtnFunc) 
    clrBtn.grid(row=1,column=1,sticky="NSEW") 
    eviBtn = tkinter.Button(root, text="Evidence", command = eviBtnFunc) 
    eviBtn.grid(row=2,column=0,sticky="NSEW")
    
    dontBtn = tkinter.Button(root, text="Evidence Needed:", command = dontClick) 
    dontBtn.grid(row=2,column=1,sticky="NSEW")
    
    
    ghost_list = tkinter.Listbox(root)
    ghost_list.grid(row=3,column=0,sticky="NSEW") 
 
    evidence_list = tkinter.Listbox(root)
    evidence_list.grid(row=3,column=1,sticky="NSEW") 
    ghost_list.bind('<<ListboxSelect>>',CurSelet)
    root.title("C69 PhasmoTool")
    photo = tkinter.PhotoImage(file="image0.png")
    root.iconphoto(False, photo)
    root.mainloop()

else:
    raise Exception("This file cannot be imported")