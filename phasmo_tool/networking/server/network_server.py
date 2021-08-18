from _thread import *
import socket
import UPL

class ServerCode:
    def __init__(self, host:str, port:int, config:dict) -> None:
        self.host   = host
        self.port   = port
        self.config = config
        
        self.connections = {}
        self.rooms = {
            "room_id" : []
        }
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.serverSocket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))

    def process_packet(self, connection:socket.socket, bufSize=1024) -> None:
        packet_data = connection.recv(bufSize).decode('utf-8')
        
        packet_data = eval(packet_data)
        return packet_data
        
    def broadcastMessage(self, message:str, room:str) -> None:
        if room not in self.rooms.keys():
            print(f"Room {room} does not exist")
            return
        
        room_users = self.rooms[room]
        for conn in room_users.keys():
            if type(message) == str:
                message = message.encode('utf-8')
            conn.send(message)
    
    def ThreadedClient(self, connection:socket.socket, address:str) -> None:
        connection.send("NAME".encode('utf-8'))
        name = self.process_packet(connection, 2048)
        
        connection.send("ROOMCODE".encode("utf-8"))
        current_room = self.process_packet(connection, 2048)
        
        if current_room in self.rooms:
            connection.send("SERVER_ACCEPTED".encode('utf-8'))
        
        else:
            connection.send("SERVER_DECLINE".encode('utf-8'))
            connection.close()
            
        try:
            while True:
                packet_data = self.process_packet(connection)
                
                data = packet_data["data"]
                print(packet_data)
                
                if packet_data['type'] == 'CHAT':
                    if len(data) > 2048:
                        data = data[:2048]
                    
                    
                        
                elif packet_data['type'] == "ACTION":
                    if data.startswith("DISCONNECT"):
                        pass
                    
        
        except Exception as e:
            pass
    
    def serverMain(self) -> None:
        print("Waiting for connections....")
        self.serverSocket.listen(5)
        
        while True:
            Client, address = self.serverSocket.accept()
            print(f"Connected to: {address[0]}:{address[1]}")
            start_new_thread(self.ThreadedClient, (Client, address))

        self.serverSocket.close()
        
def startServer(config:dict) -> None:
    HOST = "127.0.0.1" #config["Host"]
    PORT = 1222 #config["Port"]
    server = ServerCode(HOST, PORT, config)
    server.serverMain()
    
if __name__ == "__main__":
    CONFIG = UPL.Core.file_manager.getData_json("json/serverConfig.json")
    startServer(CONFIG)