import socket
import pickle
import threading

global samplelist
samplelist = []

# Function to send a list to the client
def send_list_to_client(client_socket):
    global samplelist
    # Serialize the list using pickle
    serialized_list = pickle.dumps(samplelist)
    
    # Send the serialized list to the client
    client_socket.sendall(serialized_list)

# Function to handle each client connection
def handle_client(client_socket, address, connected_clients):
    print(f"[+] {address} connected.")
    
    # Add the client to the list of connected clients
    connected_clients.append((client_socket, address))
    
    # Display the list of connected clients
    print("Connected clients:", [addr for _, addr in connected_clients])
    
    # Send a list to the client
    send_list_to_client(client_socket)
    
    # Keep the connection alive until the client disconnects
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received data from {address}: {data}")

        # Check if the client sent a query for the list
        if data.strip().lower() == b'query_list':
            send_list_to_client(client_socket)
    
    # Remove the client from the list of connected clients when they disconnect
    connected_clients.remove((client_socket, address))
    print(f"[-] {address} disconnected.")
    print("Connected clients:", [addr for _, addr in connected_clients])
    client_socket.close()

def main():
    # Define host and port
    host = '192.168.8.186'
    port = 12345

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"[*] Listening on {host}:{port}")

    # List to keep track of connected clients
    connected_clients = []

    while True:
        # Accept incoming connection
        client_socket, address = server_socket.accept()
        samplelist.append(address)
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, connected_clients))
        client_thread.start()

if __name__ == "__main__":
    main()
