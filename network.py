import socket
import pickle


# Create the "Network" class. This is the code that sets up the client for network communication.
class Network:
    # Initialize the network
    def __init__(self):
        # Create a socket using the given address family (socket.AF_INET) and socket type (socket.SOCK_STREAM) to facilitate network communications
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The IPv4 address of the server
        self.server = "3.21.40.61"  # "192.168.1.25"  # "138.236.188.50"
        # The network port through which to communicate
        self.port = 5555
        # Create the address by combining the server IPv4 address and the port
        self.addr = (self.server, self.port)
        # Call the network class function "connect" to create the connection to the server
        self.p = self.connect()

    # Function returns this client's character data.
    def getP(self):
        return self.p

    # Function creates the connection between the client and the server
    def connect(self):
        # noinspection PyBroadException
        try:
            # Attempt to establish a connection to the server.
            self.client.connect(self.addr)
            # If connection attempt is successful, receive the initial player data from the server
            return pickle.loads(self.client.recv(2048))
        except:
            # If the connection attempt fails, do nothing
            pass  # NOTE: The "pass" statement does literally nothing. It is a placeholder when a statement is required for syntax, but no code needs to be executed

    # Function sends this client's character data to the server, then returns an array sent by the server containing the data for ALL characters
    def send(self, data):
        try:
            # Attempt to send the character data to the server
            self.client.send(pickle.dumps(data))
            # Receive the array from the server and return it
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            # If there is a socket error, grab the error and print it to the console
            print(e)
