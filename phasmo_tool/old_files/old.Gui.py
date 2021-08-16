"""
    Authors: Cross/Ryan & Sweden/Jerk
    Date: 8/15/2021
"""
from core import phasmoTool
from tkinter import ttk
import tkinter 
import psutil
import UPL


ghosts = UPL.Core.file_manager.getData_json("ghosts.json")
config = UPL.Core.file_manager.getData_json("conf.json")
phasTool = phasmoTool(ghosts)

def saveBtnFunc() -> None:
    if len(phasTool.possible) != 1:
        UPL.gui.popup("There are more ghosts for you to check for, or You havent inputed all the evidence", "Little issue")

    else:
        game_stats = UPL.Core.file_manager.getData_json("game_stats.json")
        currentMap = UPL.gui.confirm("Map", "What map are you playing on?", config["in_game_maps"])
        gameID = UPL.Core.generate_code(10)
        
        if textBox.size != 0:
            notes = textBox.get("1.0", "end")
            textBox.delete("1.0", 'end')
        
        else:
            notes = "NA"
        
        ghost = phasTool.display_possibleGUI()[0]
        
        if ghost in game_stats.keys():
            game_stats[ghost] += 1
        
        else:
            game_stats[ghost] = 1
        
        game_stats[gameID] = {
            "map" : currentMap,
            "ghost type" : ghost,
            "evidence" : phasTool.display_eviGUI(),
            "notes" : notes
        }
        
        UPL.Core.file_manager.write_json("game_stats.json", game_stats, 2)

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
    mode = UPL.gui.confirm('Hunters Index', "What page of you book would you like?", ["Ghosts", "Items", "Maps"])
    
    if mode == "Ghosts":
        phasTool.lookup(UPL.gui.confirm("Hunters Index", "What would you like to look up?", config['in_game_ghosts']))
        
    elif mode == "items":
        pass
    
    elif mode == "Maps":
        pass
    
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
        phasTool.possible_evidence = phasTool.default
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

def test():
    pass

def teamSelect(event):
    widget = event.widget
    selection=widget.curselection()
    picked = widget.get(selection[0])
    people_list.delete(0, people_list.size())
    
    if picked == "Devs":
        people_list.insert(0,"Cross - Python (Core)")
        people_list.insert(1,"Sweden - Python (GUI)")
    elif picked == "Artists":
        people_list.insert(0,"Aether - Icons & Loading Image")
        people_list.insert(1,"Flower - Loading Image")
    elif picked == "About":
        print("Test2")    

def tipsSelect(event):
    widget = event.widget
    selection=widget.curselection()
    picked = widget.get(selection[0])
    
    if picked == "Show us":
        UPL.gui.popup("","Show us")
    elif picked == "Spirit":
         UPL.gui.popup("if you here a singular footstep sound and then another footstep sound 2 to 15 seconds later, it's a spirit.\n","Spirits")
    elif picked == "About":
        print("Test2")   
                
if __name__ == "__main__":
     
    root = tkinter.Tk()
    tabCtrl = ttk.Notebook(root)
    noteFrame = tkinter.Frame(root) 
    
    ## Notes page
    textBox = tkinter.Text(noteFrame)
    textBox.grid(row=0,column=0,sticky="NSEW")
    
    ## About frame 
    aboutFrame = tkinter.Frame(root) 
    teamStrVar = tkinter.StringVar() 
    peopleStrVar = tkinter.StringVar() 
    teamlbl = tkinter.Label(aboutFrame,textvariable=teamStrVar)
    teamStrVar.set("C69 Team:")
    teamlbl.grid(row=1,column=0,sticky="NSEW") 
    peoplelbl = tkinter.Label(aboutFrame,textvariable=peopleStrVar)
    peopleStrVar.set("People:")
    peoplelbl.grid(row=1,column=1,sticky="NSEW") 
    team_list = tkinter.Listbox(aboutFrame)
    team_list.grid(row=2,column=0,sticky="NSEW") 
    team_list.insert(0,"Devs")
    team_list.insert(1,"Artists")
    team_list.insert(2,"About")
    team_list.bind('<<ListboxSelect>>',teamSelect)
    people_list = tkinter.Listbox(aboutFrame)
    people_list.grid(row=2,column=1,sticky="NSEW") 
    
    ##Tips frame
    tipsFrame = tkinter.Frame(root)    
    tips_list = tkinter.Listbox(tipsFrame)
    tips_list.insert(0,"Show us")
    tips_list.insert(1,"Spirit")
    tips_list.insert(2,"")
    tips_list.bind('<<ListboxSelect>>',tipsSelect)
    tips_list.pack()
    
    ## stats frame
    statsFrame = tkinter.Frame(root)
    addBtn = tkinter.Button(statsFrame, text="Add Evidence", command = test) 
    addBtn.grid(row=0,column=0,sticky="NSEW")
    
    ## evidence frame
    eviFrame = tkinter.Frame(root)
    eviFrame.grid(row=0,column=0,sticky="NSEW")
    addBtn = tkinter.Button(eviFrame, text="Add Evidence", command = addBtnFunc) 
    addBtn.grid(row=0,column=0,sticky="NSEW")
    remBtn = tkinter.Button(eviFrame, text="Remove Evidence", command = remBtnFunc) 
    remBtn.grid(row=0,column=1,sticky="NSEW")
    lookBtn = tkinter.Button(eviFrame, text="Lookup", command = lookBtnFunc) 
    lookBtn.grid(row=1,column=0,sticky="NSEW")
    clrBtn = tkinter.Button(eviFrame, text="Clear", command = clearBtnFunc) 
    clrBtn.grid(row=1,column=1,sticky="NSEW") 
    eviBtn = tkinter.Button(eviFrame, text="Evidence", command = eviBtnFunc) 
    eviBtn.grid(row=2,column=0,sticky="NSEW")
    dontBtn = tkinter.Button(eviFrame, text="Save stats", command = saveBtnFunc) 
    dontBtn.grid(row=2,column=1,sticky="NSEW")
    ghost_list = tkinter.Listbox(eviFrame)
    ghost_list.grid(row=3,column=0,sticky="NSEW") 
    evidence_list = tkinter.Listbox(eviFrame)
    evidence_list.grid(row=3,column=1,sticky="NSEW") 
    ghost_list.bind('<<ListboxSelect>>',CurSelet)
    eviFrame.pack()
   
    ## other stuff
    tabCtrl.add(eviFrame,text='Evidence') 
    tabCtrl.add(noteFrame,text='Notes')
    #tabCtrl.add(statsFrame,text='Stats')
    tabCtrl.add(tipsFrame,text='Tips')
    tabCtrl.add(aboutFrame,text='About')
    tabCtrl.pack(expand=1,fill="both")
    
    ## window stuff
    root.resizable(False, False)
    root.geometry("256x260")
    root.title("C69 PhasmoTool")
    photo = tkinter.PhotoImage(file="icon.png")
    root.iconphoto(False, photo)
    root.mainloop()

    root.mainloop()

else:
    raise Exception("This file cannot be imported")