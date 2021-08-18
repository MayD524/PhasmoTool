from tkinter.constants import DISABLED, END
from main_gui import phasmoToolGui
from core import phasmoTool
import threading
import socket
import UPL

"""
    CREATE_ROOM > 10 digit Code
    JOIN_ROOM:<CODE> > put in room
    SEND_MSG:<MSG> > Put msg in chat
    SEND_LOG:<LOG> > Send Evidence/objectivs
    LEAVE_ROOM > Leaves Room
    
"""

class C69_phasmoTool_networking:
    def __init__(self, 
                 client_name:str, 
                 pTool:phasmoTool,
                 guiClass:phasmoToolGui,
                 IP:str,
                 PORT:int) -> None:
        self.client_name = client_name
        self.pTool       = pTool
        self.pGui        = guiClass
        self.IP          = IP
        self.PORT        = PORT
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.IP, self.PORT))
        
        rcv = threading.Thread(target=self.recv_thread)
        rcv.start()
    
    def sendBtnFunc(self, msg:str) -> None:
        ## disable text box
        self.msg = msg
        
        snd = threading.Thread(target=self.send_msg)
        snd.start()
    
    def sendPacket(self, data:str, msgType:str) -> None:
        if data == '':
            UPL.gui.popup("You cannot send null data", "Something Went Wrong")

        packet  = {
            "data" : data,
            "type" : msgType,
            "from" : self.client_name
        }
    
        message = str(packet).encode("utf-8")
        
        while True:
            self.sock.send(message)
            break
    
    def send_msg(self, *args):
        if not self.msg:
            ## get message from entry
            pass
        
        ## don't send empty msg
        if self.msg == '':
            return
        
        ## send chats
        self.pGui.textBox.config(state=DISABLED)
        self.sendPacket(self.msg, "CHAT")
        self.pGui.sendField.delete(0, END)
        self.msg = None
        ## clear 
         
    def recv_thread(self) -> str:
        temp = None
        while True:
            try:
                message = self.sock.recv(2048).decode('utf-8')
                
                message = message.replace("SERVER_ACCEPTED", "") if "SERVER_ACCEPTED" in message else message
                
                
            except Exception as e:
                pass
    
if __name__ == "__main__":
    C69_phasmoTool_networking("userName","127.0.0.1", 1222)