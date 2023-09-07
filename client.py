# Greisy Virgen Larios
# CS372 - Client Server Chat
# The TCPClient.py code on page 161 from the book of
# James F. Kurose & Keith W. Ross "Computer Networking"
# and Project 1 was used as a guide to create this program.

from socket import *

server_name = 'Rock, Paper, Scissors Server'
server_port = 4587

# Creating the socket and connecting to the determined server name and port.
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1', server_port))

# instructions = "Let's play a game of Rock, Paper, Scissors.\n" \
#                "After you make a selection, you will wait on the selection from the server" \
#                " and then the winner will be determined." \
#                "\nPlease type your selection: 'rock', 'paper', 'scissors'."

print(f"Welcome to the {server_name}!")
print("What would you like to do today?")
print("To Play 'Rock, Paper, Scissors' please type 'play'")
# print("To terminate the connection, please type '/q'.")

gameChoice = ["rock", "paper", "scissors"]

# Constant loop to print all the data,
# loop terminates once all data was received.
while True:
    # Since client acts first, I want it to get input first from the user
    print("To terminate the connection, please type '/q'.")
    client_mes = input("Enter Input > ")
    # print("Waiting for server to reply...")

    # Connection broke if 0 bytes meant to be sent
    if client_mes == "":
        print("Connection has broken.")
        break

    # to make sure to read properly
    clientM = client_mes.strip().lower()

    client_socket.send(client_mes.encode())

    if clientM == "/q":
        print("Bye bye!")
        break

    print("Waiting for server to reply...")
    serverM = client_socket.recv(4096).decode()
    print(serverM)

    # Cleaning the serve message for analyzing
    serverM = serverM.strip().lower()

    # Connection broke if 0 bytes received
    if serverM == "":
        print("Connection has broken.")
        break

    if serverM == "/q":
        print("Server is terminating the connection. Bye bye!")
        break

# Close the connection if the client sent M
client_socket.close()
