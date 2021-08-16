from core import phasmoTool
from tkinter import ttk
import tkinter 
import psutil
import UPL


class phasmoToolGui:
    def __init__(self):
        self.ghosts = UPL.Core.file_manager.getData_json("ghosts.json")
        self.config = UPL.Core.file_manager.getData_json("conf.json")
        self.phasTool = phasmoTool(self.ghosts)
        self.layout()
        self.root.mainloop()

    
    def layout(self):
        self.root = tkinter.Tk()
        self.tabCtrl = ttk.Notebook(self.root)
        self.noteFrame = tkinter.Frame(self.root) 

        ## Notes page
        self.textBox = tkinter.Text(self.noteFrame)
        self.textBox.grid(row=0,column=0,sticky="NSEW")

        ## About frame 
        self.aboutFrame = tkinter.Frame(self.root) 
        self.teamStrVar = tkinter.StringVar() 
        self.peopleStrVar = tkinter.StringVar() 
        self.teamlbl = tkinter.Label(self.aboutFrame,textvariable=self.teamStrVar)
        self.teamStrVar.set("C69 Team:")
        self.teamlbl.grid(row=1,column=0,sticky="NSEW") 
        self.peoplelbl = tkinter.Label(self.aboutFrame,textvariable=self.peopleStrVar)
        self.peopleStrVar.set("People:")
        self.peoplelbl.grid(row=1,column=1,sticky="NSEW") 
        self.team_list = tkinter.Listbox(self.aboutFrame)
        self.team_list.grid(row=2,column=0,sticky="NSEW") 
        self.team_list.insert(0,"Devs")
        self.team_list.insert(1,"Artists")
        self.team_list.insert(2,"About")
        self.team_list.bind('<<ListboxSelect>>',self.teamSelect)
        self.people_list = tkinter.Listbox(self.aboutFrame)
        self.people_list.grid(row=2,column=1,sticky="NSEW") 

        ##Tips frame
        self.tipsFrame = tkinter.Frame(self.root)    
        self.tips_list = tkinter.Listbox(self.tipsFrame)
        self.tips_list.insert(0,"Show us")
        self.tips_list.insert(1,"Spirit")
        self.tips_list.insert(2,"")
        self.tips_list.bind('<<ListboxSelect>>',self.tipsSelect)
        self.tips_list.pack()

        ## stats frame
        self.statsFrame = tkinter.Frame(self.root)
        self.addBtn = tkinter.Button(self.statsFrame, text="Add Evidence", command = self.test) 
        self.addBtn.grid(row=0,column=0,sticky="NSEW")

        ## evidence frame
        self.eviFrame = tkinter.Frame(self.root)
        self.eviFrame.grid(row=0,column=0,sticky="NSEW")
        self.addBtn = tkinter.Button(self.eviFrame, text="Add Evidence", command = self.addBtnFunc) 
        self.addBtn.grid(row=0,column=0,sticky="NSEW")
        self.remBtn = tkinter.Button(self.eviFrame, text="Remove Evidence", command = self.remBtnFunc) 
        self.remBtn.grid(row=0,column=1,sticky="NSEW")
        self.lookBtn = tkinter.Button(self.eviFrame, text="Lookup", command = self.lookBtnFunc) 
        self.lookBtn.grid(row=1,column=0,sticky="NSEW")
        self.clrBtn = tkinter.Button(self.eviFrame, text="Clear", command = self.clearBtnFunc) 
        self.clrBtn.grid(row=1,column=1,sticky="NSEW") 
        self.eviBtn = tkinter.Button(self.eviFrame, text="Evidence", command = self.eviBtnFunc) 
        self.eviBtn.grid(row=2,column=0,sticky="NSEW")
        self.dontBtn = tkinter.Button(self.eviFrame, text="Save stats", command = self.saveBtnFunc) 
        self.dontBtn.grid(row=2,column=1,sticky="NSEW")
        self.ghost_list = tkinter.Listbox(self.eviFrame)
        self.ghost_list.grid(row=3,column=0,sticky="NSEW") 
        self.evidence_list = tkinter.Listbox(self.eviFrame)
        self.evidence_list.grid(row=3,column=1,sticky="NSEW") 
        self.ghost_list.bind('<<ListboxSelect>>',self.CurSelet)
        self.eviFrame.pack()
        
        ## other stuff
        self.tabCtrl.add(self.eviFrame,text='Evidence') 
        self.tabCtrl.add(self.noteFrame,text='Notes')
        
        #tabCtrl.add(statsFrame,text='Stats')
        self.tabCtrl.add(self.tipsFrame,text='Tips')
        self.tabCtrl.add(self.aboutFrame,text='About')
        self.tabCtrl.pack(expand=1,fill="both")

        ## window stuff
        self.root.resizable(False, False)
        self.root.geometry("256x260")
        self.root.title("C69 PhasmoTool")
        self.photo = tkinter.PhotoImage(file="icon.png")
        self.root.iconphoto(False, self.photo)
    
    
    def saveBtnFunc(self) -> None:
        if len(self.phasTool.possible) != 1:
            UPL.gui.popup("There are more ghosts for you to check for, or You havent inputed all the evidence", "Little issue")

        else:
            game_stats = UPL.Core.file_manager.getData_json("game_stats.json")
            currentMap = UPL.gui.confirm("Map", "What map are you playing on?", self.config["in_game_maps"])
            gameID = UPL.Core.generate_code(10)
            
            if self.textBox.size != 0:
                notes = self.textBox.get("1.0", "end")
                self.textBox.delete("1.0", 'end')
            
            else:
                notes = "NA"
            
            ghost = self.phasTool.display_possibleGUI()[0]
            
            if ghost in game_stats.keys():
                game_stats[ghost] += 1
            
            else:
                game_stats[ghost] = 1
            
            game_stats[gameID] = {
                "map" : currentMap,
                "ghost type" : ghost,
                "evidence" : self.phasTool.display_eviGUI(),
                "notes" : notes
            }
            
            UPL.Core.file_manager.write_json("game_stats.json", game_stats, 2)

    def addBtnFunc(self) -> None:
        self.phasTool.add_evidence()
        self.ghost_list.delete(0, self.ghost_list.size())
        self.update_Ghosts()
        
    def remBtnFunc(self) -> None:
        self.phasTool.rem_evidence()
        self.ghost_list.delete(0, self.ghost_list.size())
        self.update_Ghosts()
        if self.ghost_list.size() == 0:
            self.evidence_list.delete(0, self.evidence_list.size())
        
    def lookBtnFunc(self) -> None:
        mode = UPL.gui.confirm('Hunters Index', "What page of you book would you like?", ["Ghosts", "Items", "Maps"])
        
        if mode == "Ghosts":
            self.phasTool.lookup(UPL.gui.confirm("Hunters Index", "What would you like to look up?", self.config['in_game_ghosts']))
            
        elif mode == "items":
            pass
        
        elif mode == "Maps":
            pass
        
    def eviBtnFunc(self) -> None:
        if self.phasTool.current_round != []:
            msg = "\n\t".join(self.phasTool.current_round)
            UPL.gui.popup(msg=f"Current Evidence:\n\t{msg}", title="Current Evidence")
        
        else:
            UPL.gui.popup("Go find some evidence!", title="Current Evidence")

    def clearBtnFunc(self) -> None:
        choice = UPL.gui.confirm("Clear", "Do you want this to clear the evidence?", ["Yes", "No"])
        if choice == "Yes":
            
            print(self.evidence_list.size())
            self.evidence_list.delete(0, self.evidence_list.size())
            self.ghost_list.delete(0, self.ghost_list.size())
            self.phasTool.possible_evidence = self.phasTool.default
            self.phasTool.current_round.clear()
            self.phasTool.current_guess()
            
        elif choice == "No":
            print("Not clearing")
        else:
            print(chr(69))

    def update_Ghosts(self):
        index = 0
        for ghost in self.phasTool.possible:
            self.ghost_list.insert(index, ghost)
            index += 1

    def update_Evidence(self, ghost:str) -> None:
        self.evidence_list.delete(0, self.evidence_list.size())
        index = 0
        for evidence in self.ghosts[ghost]["Evidence"]:
            self.evidence_list.insert(index, evidence)
            index += 1
            
    def CurSelet(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection[0])
        self.update_Evidence(picked)

    def dontClick(self) -> None:
        self.phasTool.clicks += 1
        if self.phasTool.clicks == 199:
            UPL.gui.popup("Dont click one more time or i will close phasmo","Dont do it")
        
        elif self.phasTool.clicks == 200:
            for proc in psutil.process_iter():
                if "phasmo" in proc.name().lower():
                    proc.kill()

    def teamSelect(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection[0])
        self.people_list.delete(0, self.people_list.size())
        
        if picked == "Devs":
            self.people_list.insert(0,"Cross - Python (Core)")
            self.people_list.insert(1,"Sweden - Python (GUI)")
        elif picked == "Artists":
            self.people_list.insert(0,"Aether - Icons & Loading Image")
            self.people_list.insert(1,"Flower - Loading Image")
        elif picked == "About":
            print("Test2")    

    def test(self): pass

    def tipsSelect(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection[0])
        
        if picked == "Show us":
            UPL.gui.popup("","Show us")
        elif picked == "Spirit":
            UPL.gui.popup("if you here a singular footstep sound and then another footstep sound 2 to 15 seconds later, it's a spirit.\n","Spirits")
        elif picked == "About":
            print("Test2") 