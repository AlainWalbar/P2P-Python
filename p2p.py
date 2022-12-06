import socket, threading, sys

BUFFER_SIZE = 256

class P2PServer:        # Class for the P2P server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    clients_list = []       # List of clients

    def __init__(self):     # Constructor
        self.sock.bind(('0.0.0.0', 8000))       # Bind to port 8000
        self.sock.listen(1)         # Listen for connections

    def handler(self, c, addr):        # Handler for client connections
        while True:          # Loops forever
            d = c.recv(BUFFER_SIZE).decode()       # Get the destination
            d = int(d)        # Convert to int
            dest = self.clients_list[d]
            # print the address of the destination
            print("Destination: ", self.getPeerAddr(dest))
            
            ftype = c.recv(BUFFER_SIZE).decode()          # Receive data from client
            ftype = int(ftype)        # Convert data to int
            
            if ftype == 4: 
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")      # Print that the client disconnected
                self.clients_list.remove(c)         # Remove the client from the list
                c.close()       # Close the connection
                break       # Exit the loop
            
       
            if ftype == 2:   # if the data received is an image file
                d = c.recv(BUFFER_SIZE).decode()
                img = open(d, 'rb')
                   
                while True:
                    data = img.readline(BUFFER_SIZE)
                    if not data:
                        break
                    dest.send(data)
                img.close()
                print("Image sent")
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")
                self.clients_list.remove(c)
                c.close()
                break
                   
            if ftype == 3:
                msg = c.recv(BUFFER_SIZE).decode()       # Receive data from client
                dest.send(msg.encode())        # except the one sending the data
                print("Message sent")
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")
                self.clients_list.remove(c)
                c.close()
                break

    def getPeerAddr(self, c):       # Function to get the address of the client
        return c.getpeername()

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
        

        dest = input ("Enter the destination: ")     # Get the destination port
        self.sock.send(dest.encode())
        file = input("What file do you wanna send?\n >1 CSV/JSON file\n >2 IMG file\n >3 Simple string message\n >4 Disconnect\n")     # Ask the user what file they want to send
        
        if file == "1" or file == "2":      # If the user wants to send a csv, json or img file:
            file_name = input("Enter the file name: ")      # Ask for the file name
            
            if file == "2":     # image:
                    
                self.sock.send(file.encode())
                print("Sending file saved as: " + file_name + "\n")
                self.send_file(file_name)
                file_name = 'docs/' + file_name
                with open(file_name, 'wb') as f:
                    while True:
                        data = self.sock.recv(BUFFER_SIZE)
                        if not data:
                            break
                        f.write(data)
                f.close()

                     
        if file == "3":     # If the user wants to send a simple string message:
            self.sock.send(file.encode())
            message = input("Enter the message: ") 
            self.send_msg(message)        # Send the message
            data = self.sock.recv(BUFFER_SIZE)     # Receive data from the server
            print(str(data, 'utf-8'))       # Print the data received from the server

            
        if file == "4":
            self.sock.send(file.encode())
            print("Disconnecting...")
            self.sock.close()
                
    
    def send_msg(self, msg):     # Function for sending messages
        self.sock.send(bytes(msg, 'utf-8'))       # Send the message to the server

    def send_file(self, file_name):     # Function for sending files
        self.sock.send(file_name.encode())     # Send the file name to the server
        print("File sent successfully\n")

            





if (len(sys.argv) > 1):     # If there is a command line argument:
    client = P2PClient(sys.argv[1])     # Create a P2P client with the argument as the server address
else:       # If there is no command line argument:
    server = P2PServer()        # Create a P2P server
    server.run()        # Run the server
    