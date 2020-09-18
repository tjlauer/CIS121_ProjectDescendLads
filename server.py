import socket
from _thread import *
from player import Player
import pickle
import random
import sys

# The IPv4 address of the server
server = "138.236.188.50"  # "192.168.1.28"
# The network port through which to communicate
port = 5555

# NOTE: Values for "server" and "port" MUST match the values in "network.py"

# Create a socket using the given address family (socket.AF_INET) and socket type (socket.SOCK_STREAM) to facilitate network communications
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Attempt to bind the socket to the server IPv4 address and the port
    s.bind((server, port))
except socket.error as e:
    # If there is a socket error, grab the error and print it to the console
    str(e)

# Enable the server to start accepting new connections.
# The argument is "backlog" which specifies the number of unaccepted connections that the system will allow before refusing new connections.
s.listen(2)

# Server has started successfully. Notify the user hosting server by writing to the console.
print("Waiting for a connection, Server Started")

# Initialize the blank array that will hold ALL character data.
players = []


# Function is executed in a separate thread, as to allow multiple connections to exist within while-loops in parallel
def threaded_client(conn, player):
    # When the client connects for the first time, send the initial character data to the client
    conn.send(pickle.dumps(players[player]))

    # Begin a while-loop to facilitate communication with this particular client.
    # We can do a while-loop while still accepting new connections BECAUSE this function is running on a new CPU thread
    while True:
        # noinspection PyBroadException
        try:
            # Wait for the character data to be sent from the client
            data = pickle.loads(conn.recv(2048))
            # Store the new data in the players array
            players[player] = data

            # If the data is "False" (meaning there is no data)
            if not data:
                # Notify the user hosting the server that this connection has disconnected.
                print("Player "+str(player)+" Disconnected")
                # Break out of the while-loop
                break

            # Assuming the received data is good, store the players array into a temporary "reply" variable
            reply = players
            # print("Received: ", data)
            # print("Sending : ", reply)

            # Send the "reply" variable to the client so that it can update it's window with the new character positions
            conn.sendall(pickle.dumps(reply))
        except:
            # If there is some sort of error, notify the user hosting the server
            print("Unexpected error:", sys.exc_info()[0])
            # Break out of the while-loop
            break

    # Notify the user hosting the server that a client has lost connection
    print("Player "+str(player)+" Lost Connection")
    # Close the connection
    conn.close()


# Initialize the "currentPlayer" counter to keep track of which client controls which character.
currentPlayer = 0

# Constantly run a while-loop to accept new connections.
while True:
    # If a client is trying to connect to the server socket, accept it
    connection, addr = s.accept()
    # Notify the user hosting server of the new connection by writing to the console.
    print("Connected to:", addr)

    # Create temporary variables for the new character's initial values
    # All of these variables and their values are explained in "player.py" under "class Player __init__"
    newPlayer_indx = currentPlayer
    newPlayer_spawnX = random.randint(256, 1024)
    newPlayer_spawnY = -50
    newPlayer_width = 50
    newPlayer_height = 50
    newPlayer_color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
    newPlayer_kick = 0
    newPlayer_kickCheck = 0

    # Append the newly created Player class to the players array.
    players.append(Player(
        newPlayer_indx,
        newPlayer_spawnX,
        newPlayer_spawnY,
        newPlayer_width,
        newPlayer_height,
        newPlayer_color,
        newPlayer_kick,
        newPlayer_kickCheck
    ))

    # Start a new CPU thread to run the function "threaded_client" with the arguments "connection" and "currentPlayer"
    start_new_thread(threaded_client, (connection, currentPlayer))

    # Increment the currentPlayer counter to prepare for the next new connection
    currentPlayer += 1
