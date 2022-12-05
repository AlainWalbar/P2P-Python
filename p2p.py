import socket, threading, sys

class P2PServer:        # Class for the P2P server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    clients_list = []       # List of clients

    def __init__(self):     # Constructor
        self.sock.bind(('0.0.0.0', 8000))       # Bind to port 8000
        self.sock.listen(1)         # Listen for connections

    def handler(self, c, addr):        # Handler for client connections
        while True:          # Loops forever
            data = c.recv(1024)          # Receive data from client
            for connection in self.clients_list:         # Send data to all clients in the list
                connection.send(data)        # except the one sending the data
            if not data:        # If no data is received:
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")      # Print that the client disconnected
                self.clients_list.remove(c)         # Remove the client from the list
                c.close()       # Close the connection
                break       # Exit the loop

    def run(self):      # Runs the server
        while True:     # Loop forever
            c, addr = self.sock.accept()       # Accept connections
            thread = threading.Thread(target=self.handler, args=(c,addr))      # Create a thread for the client
            thread.daemon = True        # Daemonize the thread
            thread.start()      # Start the thread
            self.clients_list.append(c)     # Add the client to the list
            print(str(addr[0]) + ':' + str(addr[1]), "connected")     # Print the address of the client
 
            
class P2PClient:        # Class for the P2P client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create a socket object
    
    def __init__(self, address):     # Constructor
        self.sock.connect((address, 8000))      # Connect to the server
        while True:
            file = input("What file do you wanna send?\n >1 CSV/JSON file\n >2 IMG file\n >3 Simple string message\n")     # Ask the user what file they want to send
            
            if file == "1" or file == "2":      # If the user wants to send a file:
                file_name = input("Enter the file name: ")      # Ask for the file name
            
            # STILL TO COMPLETE
            
            if file == "3":     # If the user wants to send a simple string message:
                message = input("Enter the message: ") 
                self.send_msg(message)        # Send the message
            
            data = self.sock.recv(1024)     # Receive data from the server
            print(str(data, 'utf-8'))       # Print the data received from the server
    
    def send_msg(self, msg):     # Function for sending messages
        self.sock.send(bytes(msg, 'utf-8'))       # Send the message to the server



if (len(sys.argv) > 1):     # If there is a command line argument:
    client = P2PClient(sys.argv[1])     # Create a P2P client with the argument as the server address
else:       # If there is no command line argument:
    server = P2PServer()        # Create a P2P server
    server.run()        # Run the server
    