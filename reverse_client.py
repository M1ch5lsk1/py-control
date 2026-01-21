import socket, subprocess as sub
from requests import get 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils import cmd_formatter

class Client(socket.socket):
    def __init__(self, host, port):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.host, self. port = host, port
        self.uri = "mongodb+srv://heker:CihmCAcfLoV9vQ1M@heker.3rwzyne.mongodb.net/?appName=heker"
        self.mac_list = []
        self.device_name = ""
        self.ip = get('https://api.ipify.org').content.decode('utf8')
        
        self.db = MongoClient(self.uri, server_api=ServerApi('1'))
        self.conn = self.db.get_database("py-control").get_collection("clients")
        
        self.bind((self.host, self.port))
        
    
    def db_connect(self):
        # Send a ping to confirm a successful connection
        try:
            self.db.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            exit()
            
            
    def shell(self):
        while True:
            try:
                data, address = self.recvfrom(1024)
                print(data.decode(), address)
                self.sendto("przyszłę się pszywitać".encode(), ("127.0.0.1", address[1]))
            except KeyboardInterrupt:
                print("przerwano")
            
            
    def get_cmd_data(self, command: str, searched_key: str, case_sensitive: bool = True) -> list[str]:
        key_list = []
        command = command.split()
        out = sub.run(command, capture_output=True)
        for row in cmd_formatter(out.stdout):
            if not case_sensitive:
                row = row.lower()
                searched_key = searched_key.lower()
                
            if row.find(searched_key) != -1:
                key_list.append(row[row.find(":")+1:])
        return key_list
    
    
    def start(self):
        print(f'My public IP address is: {self.ip}')

        print(f"Klient UDP gotowy do połączenia z {self.ip}:{self.port}")
        self.db_connect()
        # Create a new client and connect to the server
    
        self.device_name = self.get_cmd_data("systeminfo", "Host Name")
        self.mac_list = self.get_cmd_data("ipconfig /all", "Physical Address")
        print(self.mac_list, self.device_name)
        
        self.shell()


if __name__ == "__main__":
    client = Client("127.0.0.1", 9999)
    client.start()