import socket, subprocess as sub
from requests import get 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import threading

SERVER_IP = '127.0.0.1' # Zmień na adres serwera, jeśli działa na innej maszynie
SERVER_PORT = 9999 

IP = get('https://api.ipify.org').content.decode('utf8')
print(f'My public IP address is: {IP}')

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Gniazdo UDP

print(f"Klient UDP gotowy do połączenia z {SERVER_IP}:{SERVER_PORT}")
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

while True:
    try:
        # 1. Pobierz dane do wysłania
        prompt = input("> ")
        if not prompt: # Zabezpieczenie przed pustym wejściem
            continue 
            
        message = prompt.encode()
        
        # # 2. WYŚLIJ dane do serwera
        client.sendto(message, (SERVER_IP, SERVER_PORT))
        
        # 3. ODBIERZ odpowiedź od serwera
        data, address = client.recvfrom(1024)
        
        # 4. Wydrukuj otrzymane dane i informację, skąd przyszły
        print(f"-> {data.decode()}")


    except Exception as e:
        print(f"Wystąpił błąd linia 47: {e}")
        break # Opuść pętlę w razie błędu

client.close()