import socket
import threading
import pickle


class TCPClient:
    def __init__(self):
        self.connected_devices = []
        self.client_device = None
        self.is_client_info_captured = False
        self.client_socket = None

    def capture_client_info(self):
        if not self.is_client_info_captured :
            self.client_device = self.connected_devices[len(self.connected_devices)-1]
            self.is_client_info_captured = True

    def receive_clients_list(self):
        data = self.client_socket.recv(1024)
        self.connected_devices = pickle.loads(data)
        self.capture_client_info()
        print("Connected clients:", self.connected_devices)

    def select_device(self):
        print("Select a device from the list:")
        while True:
            for i, device in enumerate(self.connected_devices):
                print(f"{i+1}. {device}")
            try:
                choice = int(input("Enter the number of the device to connect to (0 to refresh): "))
                if choice == 0:
                    self.client_socket.sendall(b'query_list')  # Send query command to refresh list
                    self.receive_clients_list()  # Refresh the list
                elif 1 <= choice <= len(self.connected_devices):
                    return self.connected_devices[choice - 1]
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

    def connect_to_server(self):
        server_host = '192.168.8.186'
        server_port = 12345

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((server_host, server_port))
            self.receive_clients_list()
            selected_device = self.select_device()
            return selected_device, self.client_device
        except Exception as e:
            print(f"Error: {e}")
            self.client_socket.close()
            return None



class UDPClient:
    def __init__(self, selected_device, client_device, is_new_connection):
        self.server_address,self.server_port = selected_device
        self.selected_device = selected_device
        self.client_address,self.client_port = client_device
        self.is_new_connection = is_new_connection
        if self.selected_device:
            self.connect_to_device()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.is_new_connection :
            self.sock.bind(('0.0.0.0', self.client_port))  # Bind to any available interface and port
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def connect_to_device(self):
        server_address, server_port = self.selected_device
        print(f"Connecting to {server_address}:{server_port} via UDP")
        return server_address, server_port

    def send_message(self, message):
        self.sock.sendto(message.encode(), (self.server_address, self.server_port))

    def receive_messages(self):
        try :
            while True:
                data, addr = self.sock.recvfrom(1024)
                print('\nReceived from {}: {}'.format(addr, data.decode()))
        except Exception as e:
            print("") 

    def check_connection(self):
        local_address = self.sock.getsockname()
        remote_address = (self.server_address, self.server_port)
        print(f"Local endpoint: {local_address}, Remote endpoint: {remote_address}")

if __name__ == "__main__":
   
    tcp_client = TCPClient()
    selected_device, client_device = tcp_client.connect_to_server()
    if selected_device:
        udp_client = UDPClient(selected_device, client_device, True)
        print("UDP client initialized. You can start sending messages.")

        # Check the connection
        udp_client.check_connection()

        while True:
            message = input("Type a message to send: ")
            if message == "$q" :
                selected_device = tcp_client.select_device()
                udp_client = UDPClient(selected_device, client_device, False)

            else:
                udp_client.send_message(message)

