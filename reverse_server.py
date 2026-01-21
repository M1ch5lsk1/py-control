# while True:
#     prompt = input("> ")

import socket
from requests import get

class Server(socket.socket):
    def __init__(self, port: int, host: str = "127.0.0.1"):
        self.closing_attempts = 0
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.host, self.port = host, port
        self.router_IP = get('https://api.ipify.org').content.decode('utf8') 
        # self.settimeout(1)
        self.start()
        
        
    def shell(self):
        while True:
            try:
                prompt = input("prompt something> ")
                self.sendto(prompt.encode(), ("127.0.0.1", self.port))
                data, address = self.recvfrom(1024)
                print(data.decode())
            except KeyboardInterrupt:
                if self.closing_attempts == 0:
                    print("\n\n[Wciśnij Ctrl+C drugi raz aby zamknąć program.]\n")
                self.closing_attempts += 1
                if self.closing_attempts == 1:
                    break
                if self.closing_attempts == 2 :
                    print("\n\n[Zamykanie programu.]")
                    return 0
                
            except ConnectionResetError:
                print("\n[Brak ustanowionego połączenia z klientem.]\n")
    def start(self):
        print("Py-Control reverse shell\n")
        self.shell()
        
        
if __name__ == "__main__":
    server = Server(port = 9999, host = "127.0.0.1")
    server.start()
        