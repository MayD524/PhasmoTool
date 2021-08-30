"""
    Authors: Cross/Ryan & Sweden/Jerk
    Date: 8/15/2021
"""
try:
    import UPL

except ImportError:
    import sys, os
    print(chr(69))
    os.system(f"{sys.executable} ./auto_upl.py")
    os.system(f"{sys.executable} -m pip install psutil")
    import UPL
import sys

class phasmoTool:
    def __init__(self, ghosts:dict) -> UPL.null:
        """
            @params:
                ghosts (dict) : every ghost in phasmo
                
            @returns:
                None
            the init method
        """
        self.ghosts = ghosts
        self.possible = []
        self.ghosts_sep = {
            "emf level 5"           : [],
            "fingerprints"          : [],
            "spirit box"            : [],
            "ghost writing"         : [],
            "ghost orb"             : [],
            "freezing temperatures" : [],
            "dots projector"        : []
        }
        self.current_round = []
        self.default = ["fingerprints", "ghost orb", "spirit box", "freezing temperatures", "emf level 5", "ghost writing", "dots projector"]
        self.possible_evidence = self.default
        self.clicks = 0
        self.groupGhosts()
        
    def groupGhosts(self) -> UPL.null:
        """
            @params:
                None
                
            @returns:
                None
        
            groups the ghosts into different catagories based off of what evidence
            each ghost has
        """
        for ghost in self.ghosts.keys():
            for evidence in self.ghosts[ghost]["Evidence"]:
                self.ghosts_sep[evidence.lower()].append(ghost)
    
    def get_evidenceType(self, evidence:str) -> str:
        evidence = evidence.lower()
        if "finger" in evidence or "print" in evidence or "hand" in evidence:
            return "fingerprints"
        
        elif "orb" in evidence:
            return "ghost orb"
        
        elif "spirit" in evidence or "box" in evidence:
            return "spirit box"
        
        elif "freezing" in evidence or "temp" in evidence:
            return "freezing temperatures"
        
        elif "emf" in evidence:
            return "emf level 5"
        
        elif "writ" in evidence:
            return "ghost writing"
        
        elif "dots" in evidence:
            return "dots projector"
        
        else:
            return False
        
    def lookup(self, ghost:str) -> UPL.null:
        ghost = ghost.lower().capitalize()
        if ghost in self.ghosts:
            msg = f"Description : {self.ghosts[ghost]['Description']}\nStrength : {self.ghosts[ghost]['Strength']}\nWeakness : {self.ghosts[ghost]['Weakness']}\nEvidence:\n\t{self.ghosts[ghost]['Evidence'][0]}\n\t{self.ghosts[ghost]['Evidence'][1]}\n\t{self.ghosts[ghost]['Evidence'][2]}"   
            UPL.gui.popup(title=ghost, msg=msg)
        
        else:
            UPL.gui.popup(title="Unknown ghost type", msg=f"The ghost {ghost} is not known")  
    
    def add_evidence(self) -> UPL.null:
        #print(self.possible_evidence)
        if self.possible_evidence == None:
            self.possible_evidence = self.default
        evidence = UPL.gui.confirm("Select Evidence", "What evidence have you collected hunter?", self.possible_evidence)
        evidence = self.get_evidenceType(evidence)
        
        if evidence == False:
            UPL.gui.popup("That evidence does not exist")
            return
        
        if evidence not in self.current_round:
            self.current_round.append(evidence)
            self.current_guess()
            tmp = []

            for ghost in self.possible:
                evi = self.ghosts[ghost]['Evidence']
                for i in evi:
                    if i.lower() == evidence:
                        continue
                    elif i.lower() in self.current_round:
                        continue
                    
                    elif i not in tmp:
                        tmp.append(i)
         
            self.possible_evidence = tmp

    def rem_evidence(self) -> UPL.null:
        evidence = UPL.gui.confirm("Select Evidence", "What evidence have you collected hunter?", self.current_round)
        evidence = self.get_evidenceType(evidence)
        
        if evidence == False:
            UPL.gui.popup("That evidence does not exist")
            return
        
        if evidence in self.current_round:
            self.current_round.remove(evidence)
            self.current_guess()
            tmp = []
            for ghost in self.possible:
                evi = self.ghosts[ghost]['Evidence']
                for i in evi:
                    if i.lower() in self.current_round:
                        continue
                    
                    elif i.lower() not in tmp:
                        tmp.append(i)
            tmp = list(set(tmp))  
            if tmp != []:
                tmp = tmp.sort()          
            self.possible_evidence = tmp
            
        self.current_guess()
            
    
    ## possible ghosts
    def display_possibleGUI(self) -> list:
        return self.possible
    
    ## all evidence
    def display_eviGUI(self) -> list:
        return self.current_round
    
    def display_possible(self) -> UPL.null:
        """
            @params:
                None
                
            @returns:
                None
            
            displays all the possible ghosts
        """
        print("All possible ghosts:")
        if len(self.possible) == 1:
            print(f"The ghost is a {self.possible[0]}")
            return
        
        elif len(self.possible) == 0:
            print("Go find some evidence!")
            return        
        
        for ghost in self.possible:
            tmp = [i for i in self.ghosts[ghost]["Evidence"] if i.lower() not in self.current_round]
            print(f"\t{ghost} : {tmp}")
            
    def current_guess(self) -> UPL.null:
        """
            @params:
                None
                
            @returns:
                None
            
            Attempts to figure out what the ghost may be
        """
        possible = []
        for evidence in self.ghosts_sep.keys():
            if evidence in self.current_round:
                if len(possible) > 0:
                    possible = [i for i in self.ghosts_sep[evidence] if i in possible]
                else:
                    possible = self.ghosts_sep[evidence]
                    
        if possible != []:
            self.possible = possible
        else:
            self.possible = self.ghosts.keys() 
    
    ## command line specific
    def displayHelp(self) -> UPL.null:
        print("[add] Add Evidence\n[rem] Remove Evidence\n[look] Ghost Lookup\n[ghosts] Display all possible ghosts\n[evi] Display all current evidences\n[clear] Clears the screen\n[help] Display help\n[exit] Exits")
        
    def main(self) -> UPL.null:
        """
            @params:
                None
                
            @returns:
                None
                
            Runs all the time and gets user input
        """
        self.displayHelp()
        while True:
            
            ## get user input
            user_inp = UPL.Core.ainput("> ", str, 3).lower()
            
            if user_inp == "exit":
                sys.exit(0)
            
            elif user_inp == "ghosts":
                self.display_possible()
                continue
            
            elif user_inp == "evi":
                print("All collected evidence: ")
                for evidence in self.current_round:
                    print(f"\t{evidence}")
                
                continue
              
            elif user_inp == "clear":
                UPL.Core.clear()
                continue  
            
            cmd, data = user_inp.split(" ", 1)
            

            if cmd == "add":
                data = self.get_evidenceType(data)
                if data not in self.current_round:
                    self.current_round.append(data)
                    
                self.current_guess()
                self.display_possible()
                
            elif cmd == "rem":
                data = self.get_evidenceType(data)
                if data in self.current_round:
                    self.current_round.remove(data)
                
                self.current_guess()
                self.display_possible()
                    
            elif cmd == "look":
                data = data.lower().capitalize()
                if data in self.ghosts.keys():
                    print(f'{data}:\n\tDescription: {self.ghosts[data]["Description"]}\n\tStrength: {self.ghosts[data]["Strength"]}\n\tWeakness: {self.ghosts[data]["Weakness"]}\nEvidence:\n\t{self.ghosts[data]["Evidence"][0]}\n\t{self.ghosts[data]["Evidence"][1]}\n\t{self.ghosts[data]["Evidence"][2]}')
                    
                else:
                    print("What the kinda ghost is that...")
                
            elif cmd == "help":
                self.displayHelp()
                
            else:
                pass

## !! START !! ##
if __name__ == "__main__":
    ghost_data = UPL.Core.file_manager.getData_json("ghosts.json")
    tool = phasmoTool(ghost_data)
    tool.main()