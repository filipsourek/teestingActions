import socket, threading
from bot import Bot

print("[STARTING] server is starting...")
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

SERVER = ''
IP = socket.gethostbyname(SERVER)
PORT = 5555 
ADDR = (SERVER, PORT)
HEADERSIZE = 5
print("[LISTENING] server is listening...")

server.bind(ADDR)
server.listen()

b = Bot()

def recv_msg(client):
    try:
        print("AHOJ")
        header = client.recv(HEADERSIZE)
        if not len(header):
            return False
        lenght = int(header.decode().strip())
        msg = client.recv(lenght).decode()
        print(msg)
        return msg
    except:
        return False

def clientThread(client):
    while True:
        try:
            msg = recv_msg(client)
            if msg is False:
                break
            print(msg)
            response = b.getResponse(msg)
            send_msg(client, response)
        except:
            break
        
def send_msg(client, msg):
    if msg:
        msg = msg.encode()
        header = f"{len(msg):<{HEADERSIZE}}".encode()
        msg = header + msg
        client.send(msg)

def run():
    while True:
        client, address = server.accept()
        
        thread = threading.Thread(target=clientThread, args=(client,))
        thread.start()

if __name__ == "__main__":
    run()
