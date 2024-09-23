import socket
import threading

# Function to handle communication with a specific client
def handle_client(client_socket, clients):
    while True:
        try:
            # Receiving message from client
            message = client_socket.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                # Broadcast the message to all other connected clients
                broadcast(message, clients, client_socket)
            else:
                clients.remove(client_socket)
                client_socket.close()
                break
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to broadcast messages to all clients
def broadcast(message, clients, sender_socket=None):
    for client in clients:
        if client != sender_socket:  # Don't send to the sender
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

# Function to allow server to send messages
def server_send_message(clients):
    while True:
        message = input("Server: ")  # Server can input messages to send
        broadcast(f"Server: {message}".encode('utf-8'), clients)

# Function to start the server
def start_server():
    server_ip = "127.0.0.1"  # localhost
    server_port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    clients = []

    # Start a thread for the server to send messages
    server_thread = threading.Thread(target=server_send_message, args=(clients,))
    server_thread.start()

    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        clients.append(client_socket)

        # Start a new thread to handle this client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients))
        client_thread.start()

if __name__ == "__main__":
    start_server()
