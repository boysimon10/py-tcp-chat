import socket
import threading

host = '127.0.0.1'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client, username):
    try:
        while True:
            message = client.recv(1024)
            broadcast(message)
    except Exception as e:
        print(f"Error with client {username}: {e}")
    finally:
        try:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                usernames.remove(username)
                broadcast(f'{username} left the chat!'.encode('utf-8'))
                print(f"{username} has disconnected")
        except Exception as e:
            print(f"Error while removing client: {e}")

def receive():
    while True:
        try:
            client, address = server.accept()
            print(f'Connected with {str(address)}')

            client.send('USERNAME'.encode('utf-8'))
            username = client.recv(1024).decode('utf-8')
            usernames.append(username)
            clients.append(client)

            print(f'{username} join the chat!')
            broadcast(f'{username} joined the chat!'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client, username))
            thread.start()
        except Exception as e:
            print(f"Error during connection: {e}")

print('Server is listening...')
try:
    receive()
except KeyboardInterrupt:
    print("Server shutdown")
    
    server.close()
    
    for client in clients:
        try:
            client.close()
        except:
            pass