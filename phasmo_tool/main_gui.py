from _thread import start_new_thread
from core import phasmoTool
from tkinter import ttk
import map_display
import subprocess
import PT_lookup
import tkinter
import psutil
import UPL
import sys
## import last due to UPL 
#from networking.client.network_client import C69_phasmoTool_networking

class phasmoToolGui:
    def __init__(self, config:dict) -> None:
        self.ghosts    = UPL.Core.file_manager.getData_json("./json/ghosts.json")
        self.tools     = UPL.Core.file_manager.getData_json("./json/tools.json")
        self.config    = config
        self.game_maps = UPL.Core.file_manager.getData_json("./json/maps.json")
        self.phasTool  = phasmoTool(self.ghosts)
        self.layout()
        
        #if self.config["allow_networking"] == True:
        #    start_new_thread(self.chat_Code, ())
            
        self.root.mainloop()

    '''def chat_Code(self) -> None:
        C69_phasmoTool_networking(
                self.config["networking_display_name"],
                self.phasTool,
                "temp_room",
                self.config["networking_host_ip"],
                self.config["networking_host_port"]
            )'''
    
    def layout(self):
        self.root = tkinter.Tk()
        
        self.tabCtrl = ttk.Notebook(self.root)
        ##Menubar 
        self.menuBar = tkinter.Menu(self.root,tearoff=0)
        self.root.config(menu=self.menuBar)
        settingsBar = tkinter.Menu(self.menuBar,tearoff=0)
        self.menuBar.add_cascade(label="Settings", menu=settingsBar)
        settingsBar.add_command(label="Open settings",command=self.openSettings)
        settingsBar.add_command(label="Restart",command=self.restartProg)
        
        ## Notes page
        self.noteFrame = tkinter.Frame(self.root) 
        self.textBox = tkinter.Text(self.noteFrame)
        self.textBox.grid(row=0,column=0,sticky="NSEW")
        
        self.noteScroolBar = tkinter.Scrollbar(self.textBox)
        self.noteScroolBar.place(relheight=1, relx=1)
        
        ## Objectives
        self.objectivesFrame = tkinter.Frame(self.root)
        self.addObjBtn = tkinter.Button(self.objectivesFrame, text="Add objective", command = self.addObjFunc) 
        self.addObjBtn.grid(row=0,column=0,sticky="NSEW")
        self.remObjBtn = tkinter.Button(self.objectivesFrame, text="Remove objective", command = self.remObjFunc) 
        self.remObjBtn.grid(row=0,column=1,sticky="NSEW")
        
        ##Chat frame
        self.chatFrame = tkinter.Frame(self.root)
        self.chatBox = tkinter.Text(self.chatFrame,width=25,height=25)
        self.chatBox.grid(row=0,column=0,sticky="NSEW")
        self.sendField = tkinter.Entry(self.chatFrame)
        self.sendField.grid(row=1,column=0,sticky="NSEW")
        self.sendBtn = tkinter.Button(self.chatFrame,text="Send message",command = self.test)
        self.sendBtn.grid(row=1,column=1,sticky="NSEW")
        
        self.chatScrollBar = tkinter.Scrollbar(self.chatBox)
        self.chatScrollBar.place(relheight=1, relx=0.974)
        
        ## About frame 
        self.aboutFrame = tkinter.Frame(self.root) 

        
        self.teamlbl = tkinter.Label(self.aboutFrame,text="C69 Team:")
        self.teamlbl.grid(row=1,column=0,sticky="NSEW") 
        
        self.peoplelbl = tkinter.Label(self.aboutFrame,text="People:")
        self.peoplelbl.grid(row=1,column=1,sticky="NSEW") 
        
        self.team_list = tkinter.Listbox(self.aboutFrame,width=40,height=15)
        self.team_list.grid(row=2,column=0,sticky="NSEW") 
        self.team_list.insert(0,"Devs")
        self.team_list.insert(1,"Artists")
        self.team_list.insert(2,"About")
        self.team_list.bind('<<ListboxSelect>>',self.teamSelect)
        self.people_list = tkinter.Listbox(self.aboutFrame,width=40,height=25)
        self.people_list.grid(row=2,column=1,sticky="NSEW") 

        ##Tips frame
        self.tipsFrame = tkinter.Frame(self.root)    
        self.tips_list = tkinter.Listbox(self.tipsFrame,width=100,height=80)
        
        for i in range(len(self.config['C69_tips'])):
            self.tips_list.insert(i, self.config['C69_tips'][i])

        self.tips_list.bind('<<ListboxSelect>>',self.tipsSelect)
        self.tips_list.pack()

        ## stats frame
        self.statsFrame = tkinter.Frame(self.root)
        self.addBtn = tkinter.Button(self.statsFrame, text="Add Evidence", command = self.test) 
        self.addBtn.grid(row=0,column=0,sticky="NSEW")

        ## evidence frame
        self.eviFrame = tkinter.Frame(self.root)
        self.eviFrame.grid(row=0,column=0,sticky="NSEW")
        
        self.addBtn = tkinter.Button(self.eviFrame, text="Add Evidence",width=45, height=5,command = self.addBtnFunc) 
        self.addBtn.grid(row=0,column=0,sticky="NSEW")
        
        self.remBtn = tkinter.Button(self.eviFrame, text="Remove Evidence",width=25, height=5, command = self.remBtnFunc) 
        self.remBtn.grid(row=0,column=1,sticky="NSEW")
        
        self.lookBtn = tkinter.Button(self.eviFrame, text="Lookup",width=10, height=5, command = self.lookBtnFunc) 
        self.lookBtn.grid(row=1,column=0,sticky="NSEW")
        
        self.clrBtn = tkinter.Button(self.eviFrame, text="Clear",width=10, height=2, command = self.clearBtnFunc) 
        self.clrBtn.grid(row=1,column=1,sticky="NSEW") 
        
        self.eviBtn = tkinter.Button(self.eviFrame, text="Evidence",width=10, height=2, command = self.eviBtnFunc) 
        self.eviBtn.grid(row=2,column=0,sticky="NSEW")
        
        self.dontBtn = tkinter.Button(self.eviFrame, text="Save stats",width=10, height=2, command = self.saveBtnFunc) 
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
        self.tabCtrl.add(self.objectivesFrame,text='Objectives')
        self.tabCtrl.add(self.chatFrame,text='Chat')
        self.tabCtrl.add(self.tipsFrame,text='Tips')
        self.tabCtrl.add(self.aboutFrame,text='About')
        self.tabCtrl.pack(expand=1,fill="both")
        #tabCtrl.add(statsFrame,text='Stats')

        ## window stuff
        self.root.resizable(False, False)
        self.root.geometry("500x500")
        self.root.title("C69 PhasmoTool")
        self.photo = tkinter.PhotoImage(file="./images/icons/icon.png")
        self.root.iconphoto(False, self.photo)
        self.root.config(menu=self.menuBar)
    
    def addObjFunc(self) -> None:
        self.names = ["Bone"]
        for i in range(3):
            opts = [x for x in self.config['in_game_objectives'] if x not in self.names]
            self.names.append(UPL.gui.confirm("Add objective", "Objective name", opts))
        
        self.objsVars = [tkinter.IntVar() for i in range(4)]
        self.objsBtns = []
        row, column = 2, 0
        for i in range(len(self.objsVars)):
            self.objsBtns.append(tkinter.Checkbutton(self.objectivesFrame,variable=self.objsVars[i],onvalue=1, offvalue=0,command=self.checkObjectives,text=self.names[i]))
            self.objsBtns[-1].grid(row=row, column=column, sticky="NSEW")
            
            if column == 1:
                row += 1;column = 0
            else:
                column += 1

    def checkObjectives(self) -> None:
        x = 0
        for i in self.objsVars:
            x += 1 if i.get() == 1 else 0
        if x == 4:
            UPL.gui.popup("You completed all the objectives","Good Job")

    def remObjFunc(self) -> None:
        list = self.objectivesFrame.grid_slaves()
        for l in list:
            l.destroy()
        self.addObjBtn = tkinter.Button(self.objectivesFrame, text="Add objective", command = self.addObjFunc) 
        self.addObjBtn.grid(row=0,column=0,sticky="NSEW")
        self.remObjBtn = tkinter.Button(self.objectivesFrame, text="Remove objective", command = self.remObjFunc) 
        self.remObjBtn.grid(row=0,column=1,sticky="NSEW")
    
    def saveBtnFunc(self) -> None:
        if len(self.phasTool.possible) != 1:
            UPL.gui.popup("There are more ghosts for you to check for, or You havent inputed all the evidence", "Little issue")

        else:
            game_stats = UPL.Core.file_manager.getData_json("./json/game_stats.json")
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
            
            UPL.Core.file_manager.write_json("./json/game_stats.json", game_stats, 2)

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
            ghost = UPL.gui.confirm("Hunters Index", "What would you like to look up?", self.config['in_game_ghosts'])
            PT_lookup.lookup_ghost(ghost, self.ghosts)
            
        elif mode == "Items":
            item = UPL.gui.confirm("Hunters Index", "What item do you want to look up?", self.config["in_game_items"])
            PT_lookup.lookup_tool(item, self.tools)
            
        elif mode == "Maps":
            map_name = UPL.gui.confirm("Hunters Index", "What map would you like to look up?", self.config["in_game_maps"])
            map_display.displayMap(map_name=map_name, map_images=self.game_maps)
    
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
        widget    = event.widget
        selection =widget.curselection()
        picked    = widget.get(selection[0])
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
        widget    = event.widget
        selection =widget.curselection()
        picked    = widget.get(selection[0])
        self.people_list.delete(0, self.people_list.size())
        
        if picked == "Devs":
            self.people_list.insert(0,"Cross - Python (Core)")
            self.people_list.insert(1,"Sweden - Python (GUI)")
        
        elif picked == "Artists":
            self.people_list.insert(0,"Daisy  - Ghost icons")
            self.people_list.insert(1,"Flower - Loading Image & ghost icons")
        
        elif picked == "About":
            self.people_list.insert(0, "We are char(69) :>")  

    def test(self): 
        print(self.sendField.get())

    def tipsSelect(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection[0])
        
        if picked == "Show us":
            UPL.gui.popup("","Show us")
        
        elif picked == "Spirit":
            UPL.gui.popup("if you here a singular footstep sound and then another footstep sound 2 to 15 seconds later, it's a spirit.\n","Spirits")
        
        elif picked == "Repel ghost with smudge":
            #Maybe?
            UPL.gui.popup("To repel the ghost with a smudge stick, you must be within \"heartbeat\" range of the ghost for it to work.")
        
        elif picked == "Spirit box mechanics":
            UPL.gui.popup("You must be either within 3 meters of the ghost or in the same room as the ghost to get a response.")
        
        elif picked == "Shades":
            UPL.gui.popup("Shades still have a VERY LOW chance of hunting when multiple people are nearby\nTho it's not impossible for it to hunt")
        
        elif picked == "Thrown items":
            UPL.gui.popup("If you're within line of sight of items being thrown, you will lose sanity (the number of items thrown x 2 = % sanity lost)")
    
        elif picked == "Attracting the ghost":
            UPL.gui.popup("If you use the Spirit Box redundantly or taunt or using trigger words.\nThat will make the ghost more likely to hunt.","C69 PhasmoTool Hits")
    
    def restartProg(self) -> None:
        
        subprocess.Popen(f"{sys.executable} ./Gui.py")
        sys.exit(0)
        
    def openSettings(self) -> None:
        self.settingsWin    = tkinter.Toplevel()
        self.debugModeTxt   = tkinter.StringVar()
        self.updateModeTxt  = tkinter.StringVar()
        self.networkModeTxt = tkinter.StringVar()
        self.networkIPIn    = tkinter.StringVar()
        self.networkPortIn  = tkinter.StringVar()
        
        self.debugModeTxt.set("Debug mode on" if self.config['debug_mode'] else "Debug mode off")
        self.debugModeToggle = tkinter.Button(self.settingsWin,textvariable=self.debugModeTxt,command=lambda: self.toggle_button("debug_mode"))
        self.debugModeToggle.grid(row=0, column=0, sticky="NSEW")

        self.updateModeTxt.set("Auto update on" if self.config['allow_auto_update'] else "Auto update off")
        self.autoModeToggle = tkinter.Button(self.settingsWin,textvariable=self.updateModeTxt,command=lambda: self.toggle_button("allow_auto_update"))
        self.autoModeToggle.grid(row=0, column=1, sticky="NSEW")
        
        self.networkModeTxt.set("Allow network on" if self.config['allow_networking'] else "Auto network off")
        self.networkModeToggle = tkinter.Button(self.settingsWin,textvariable=self.networkModeTxt,command=lambda: self.toggle_button("allow_networking"))
        self.networkModeToggle.grid(row=2, column=0, sticky="NSEW")

        self.updateNetworkBtn = tkinter.Button(self.settingsWin,text="Update network",command=self.updateNetwork)
        self.updateNetworkBtn.grid(row=2,column=1,sticky="NSEW")
        self.networkIPTxt = tkinter.Label(self.settingsWin,text="Input ip")
        self.networkIPTxt.grid(row=3, column=0, sticky="NSEW")
        
        self.networkIP = tkinter.Entry(self.settingsWin,textvariable=self.networkIPIn)
        self.networkIP.grid(row=3, column=1, sticky="NSEW")
        
        self.networkPortTxt = tkinter.Label(self.settingsWin,text="Input port")
        self.networkPortTxt.grid(row=4, column=0, sticky="NSEW")
        
        self.networkPort = tkinter.Entry(self.settingsWin,textvariable=self.networkPortIn)
        self.networkPort.grid(row=4, column=1, sticky="NSEW")
        


        self.settingsWin.title("C69 PhasmoTool")
        self.settingsWin.resizable(False, False)
        self.settingsWin.geometry("200x200")
        self.settingsWin.mainloop()
        
    def updateNetwork(self) -> None:
        if self.networkIPIn.get() == "" or self.networkPortIn.get() == "":
            UPL.gui.popup("Dont leave port or ip address empty","Error?")
        else:
            self.config["networking_host_ip"] = int(self.networkIPIn.get())
            UPL.Core.file_manager.write_json("./json/conf.json", self.config["networking_host_ip"], 2)
            self.config["networking_host_port"] = int(self.networkPortIn.get())
            UPL.Core.file_manager.write_json("./json/conf.json", self.config["networking_host_port"], 2)
            
            return
    def toggle_button(self, setting_opt:str) -> None:
        self.config[setting_opt] = not self.config[setting_opt]
        self.updateModeTxt.set("Auto update on" if self.config['allow_auto_update'] else "Auto update off")
        self.debugModeTxt.set("Debug mode on" if self.config['debug_mode'] else "Debug mode off")
        self.networkModeTxt.set("Allow network on" if self.config['allow_networking'] else "Auto network off")
        UPL.Core.file_manager.write_json("./json/conf.json", self.config, 2)
