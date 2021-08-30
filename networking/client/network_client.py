from tkinter.constants import DISABLED, END, NORMAL
import tkinter
#from main_gui import phasmoToolGui
#from core import phasmoTool
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
                 pTool,
                 RoomCode:str,
                 IP:str,
                 PORT:int) -> None:
        
        self.window = tkinter.Tk()
        self.window.resizable(False, False)
        self.window.title("C69 PhasmoTool : Chat")
        
        self.client_name = client_name
        self.pTool       = pTool
        self.roomCode    = RoomCode
        self.IP          = IP
        self.PORT        = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.IP, self.PORT))
        
        self.layout()

        rcv = threading.Thread(target=self.recv_thread)
        rcv.start()
        
        self.window.mainloop()
        rcv.join()
    
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
        self.chatBox.config(state=DISABLED)
        self.sendPacket(self.msg, "CHAT")
        self.sendField.delete(0, END)
        self.msg = None
        ## clear 
    
    def update_text(self, text:str) -> None:
        self.chatBox.config(state=NORMAL)
        self.chatBox.insert(END, text+"\n\n")
        self.chatBox.config(state=DISABLED)
        self.chatBox.see(END)
    
    def recv_thread(self) -> None:
        temp = None
        first_boot = True
        while True:
            try:
                message = self.sock.recv(2048).decode('utf-8')
                print(message)
                if first_boot:
                    if "CLIENT_NAME" in message:
                        self.sendPacket(self.client_name, "USER_DATA")
                        continue
                    
                    elif "CLIENT_ROOMCODE" in message:
                        self.sendPacket(self.roomCode, "USER_DATA")
                        first_boot = False
                        continue
                    
                
                if "SERVER_ACCEPTED" in message:
                    message = message.replace("SERVER_ACCEPTED", "") if "SERVER_ACCEPTED" in message else message
                
                elif "SERVER_DECLINED" in message:
                    pass
                
                if f"{self.client_name} has joined the room" in message:
                    temp = f"{self.client_name} has joined the room"
                    message = message.replace(temp, "")
                    self.chatBox.config(state=NORMAL)
                    self.chatBox.insert(END, temp+"\n\n")
                    self.chatBox.config(state=DISABLED)
                    self.chatBox.see(END)
                    
                elif f"{self.client_name} has left the chat" in message:
                    temp = f"{self.client_name} has left the chat"
                    message = message.replace(temp, "")
                    self.chatBox.config(state=NORMAL)
                    self.chatBox.insert(END, temp+"\n\n")
                    self.chatBox.config(state=DISABLED)
                    self.chatBox.see(END)
                
                self.chatBox.config(state=NORMAL)
                self.chatBox.insert(END, message+'\n\n')
                self.chatBox.config(state=DISABLED)
                self.chatBox.see(END)
                
            except Exception as e:
                print(e)
                # an error will be printed on the command line or console if there's an error 
                print("An error occured!") 
                self.sock.close() 
                break
    
    def layout(self) -> None:
        ##Chat frame
        
        self.chatBox = tkinter.Text(self.window,width=25,height=25)
        self.chatBox.grid(row=0,column=0,sticky="NSEW")
        self.sendField = tkinter.Entry(self.window)
        self.sendField.grid(row=1,column=0,sticky="NSEW")
        self.sendBtn = tkinter.Button(self.window,text="Send message",command =lambda: self.sendBtnFunc(self.sendField.get()))
        self.sendBtn.grid(row=1,column=1,sticky="NSEW")
        
        self.chatScrollBar = tkinter.Scrollbar(self.chatBox)
        self.chatScrollBar.place(relheight=1, relx=0.974)
        self.window.mainloop()
    
if __name__ == "__main__":
    C69_phasmoTool_networking("userName","127.0.0.1", 1222)