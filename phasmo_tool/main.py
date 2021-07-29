from pprint import pprint
import UPL
import sys

from UPL.Core import currentDir

def diff(list1:list, list2:list) -> list:
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))

class phasmoTool:
    def __init__(self, ghosts:dict) -> UPL.null:
        self.ghosts = ghosts
        self.possible = []
        self.ghosts_sep = {
            "emf level 5"           : [],
            "fingerprints"          : [],
            "spirit box"            : [],
            "ghost writing"         : [],
            "ghost orb"             : [],
            "freezing temperatures" : []
        }
        self.current_round = []
        self.groupGhosts()
        
    def groupGhosts(self) -> UPL.null:
        for ghost in self.ghosts.keys():
            for evidence in self.ghosts[ghost]["Evidence"]:
                self.ghosts_sep[evidence.lower()].append(ghost)
    
    def display_possible(self) -> UPL.null:
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
        possible = []
        for evidence in self.ghosts_sep.keys():
            if evidence in self.current_round:
                if len(possible) > 0:
                    possible = [i for i in self.ghosts_sep[evidence] if i in possible]
                else:
                    possible = self.ghosts_sep[evidence]
        self.possible = possible
    
    def displayHelp(self) -> UPL.null:
        print("[add] Add Evidence\n[rem] Remove Evidence\n[look] Ghost Lookup\n[ghosts] Display all possible ghosts\n[evi] Display all current evidences\n[clear] Clears the screen\n[help] Display help\n[exit] Exits")
        
    def main(self) -> UPL.null:
        self.displayHelp()
        while True:
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
            
            match cmd:
                case "add":
                    match data:
                        case "spirit" | "spirit box":
                            if "spirit box" not in self.current_round:
                                self.current_round.append("spirit box")
                            
                        case "writing" | "ghost writing":
                            if "ghost writing" not in self.current_round:
                                self.current_round.append("ghost writing")
                            
                        case "orbs" | "orb" | "ghost orbs" | "ghost orb":
                            if "ghost orb" not in self.current_round:
                                self.current_round.append("ghost orb")
                        
                        case "emf" | "emf 5" | "emf level 5":
                            if "emf level 5" not in self.current_round:
                                self.current_round.append("emf level 5")
                        
                        case "cold" | "freezing" | "temps" | "freezing temps" | "freezing temperatures":
                            if "freezing temperatures" not in self.current_round:
                                self.current_round.append("freezing temperatures")
                        
                        case "fingers" | "fingerprints" | "fingies" | "hand":
                            if "fingerprints" not in self.current_round:
                                self.current_round.append("fingerprints")
                    self.current_guess()
                    self.display_possible()
                
                case "rem":
                    match data:
                        case "spirit" | "spirit box":
                            if "spirit box" in self.current_round:
                                self.current_round.remove("spirit box")
                            
                        case "writing" | "ghost writing":
                            if "ghost writing" in self.current_round:
                                self.current_round.remove("ghost writing")
                            
                        case "orbs" | "orb" | "ghost orbs" | "ghost orb":
                            if "ghost orb" in self.current_round:
                                self.current_round.remove("ghost orb")
                        
                        case "emf" | "emf 5" | "emf level 5":
                            if "emf level 5" in self.current_round:
                                self.current_round.remove("emf level 5")
                        
                        case "cold" | "freezing" | "temps" | "freezing temps" | "freezing temperatures":
                            if "freezing temperatures" in self.current_round:
                                self.current_round.remove("freezing temperatures")
                        
                        case "fingers" | "fingerprints" | "fingies" | "hand":
                            if "fingerprints" in self.current_round:
                                self.current_round.remove("fingerprints")
                    self.current_guess()
                    self.display_possible()
                    
                case "look":
                    data = data.lower().capitalize()
                    if data in self.ghosts.keys():
                        print(f'{data}:\n\tDescription: {self.ghosts[data]["Description"]}\n\tStrength: {self.ghosts[data]["Strength"]}\n\tWeakness: {self.ghosts[data]["Weakness"]}\nEvidence:\n\t{self.ghosts[data]["Evidence"][0]}\n\t{self.ghosts[data]["Evidence"][1]}\n\t{self.ghosts[data]["Evidence"][2]}')
                    
                    else:
                        print("What the kinda ghost is that...")
                
                case "help":
                    self.displayHelp()
                
                ## wild card
                case _:
                    pass
        
if __name__ == "__main__":
    ghost_data = UPL.Core.file_manager.getData_json("ghosts.json")
    tool = phasmoTool(ghost_data)
    tool.main()
