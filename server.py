import socket
from _thread import *
from player import Player
import pickle
import random
import sys

# server = "192.168.1.28"
server = "138.236.188.50"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = []


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    while True:
        # noinspection PyBroadException
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Player "+str(player)+" Disconnected")
                break

            reply = players
            # print("Received: ", data)
            # print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            break

    print("Player "+str(player)+" Lost Connection")
    conn.close()


currentPlayer = 0
while True:
    connection, addr = s.accept()
    print("Connected to:", addr)

    newPlayer_indx = currentPlayer
    newPlayer_spawnX = random.randint(256, 1024)
    newPlayer_spawnY = -50
    newPlayer_width = 50
    newPlayer_height = 50
    newPlayer_color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
    newPlayer_kick = 0
    newPlayer_kickCheck = 0

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

    start_new_thread(threaded_client, (connection, currentPlayer))
    currentPlayer += 1
