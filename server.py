# Greisy Virgen Larios
# CS372 - Client Server Chat
# The TCPServer.py code on pages 163-164 from the book of
# James F. Kurose & Keith W. Ross "Computer Networking"
# and Project 1 was used as a guide to create this program.

from socket import *


def helper_validation(clientC, serverC):
    """
    Logic to determine the winner based on what was chosen by the
    client and the server on the game of rock, paper, scissors.
    """
    if clientC == "rock":
        if serverC == "paper":
            return "server"
        elif serverC == "scissors":
            return "client"
        elif serverC == "rock":
            return "draw"

    if clientC == "paper":
        if serverC == "scissors":
            return "server"
        elif serverC == "rock":
            return "client"
        elif serverC == "paper":
            return "draw"

    if clientC == "scissors":
        if serverC == "paper":
            return "client"
        elif serverC == "rock":
            return "server"
        elif serverC == "scissors":
            return "draw"


# Determining the port, creating and binding the socket to
# the given port and to the determined host.
server_port = 4587
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', server_port))
server_socket.listen()

gameChoice = ["rock", "paper", "scissors"]

instructions = "Let's play a game of Rock, Paper, Scissors.\n" \
               "After you make a selection, you will wait and then the winner will be determined." \
               "\nPlease type your selection: 'rock', 'paper', 'scissors'.\n"

# Hardcoded the printing of the host and port this server is connecting to.
print(f"Connected by ('127.0.0.1', {server_port})")

# Storing the new socket and address once we accept from our server socket.
connection_socket, connection_address = server_socket.accept()

# helps me avoid a double printing issue with the instructions
playingGame = False


while True:
    print("Waiting for message from Client...")
    # print("Type '/q' to terminate the connection.")
    clientM = connection_socket.recv(4096).decode()

    # Cleaned up client for error checking:
    cleanClient = clientM.strip().lower()

    # Connection broke if 0 bytes meant to be sent
    if clientM == "":
        print("Connection has broken.")
        break

    elif cleanClient == "/q":
        print("The client is terminating the connection. Bye bye!")
        break

    elif cleanClient == "play":
        playingGame = True
        print("You will receive the instructions once client makes their choice.")
        # Send the client that we are playing the game, so send instructions.
        connection_socket.send(instructions.encode())

    elif cleanClient not in gameChoice and playingGame is True:
        badInput = "Please enter a valid choice: 'rock', 'paper', 'scissors'"
        connection_socket.send(badInput.encode())
        print(f"Client entered invalid input: '{clientM}', wait for them to re-enter a choice...")

    elif cleanClient in gameChoice and playingGame is True:
        # Using the flag I set, helps me avoid double printing of instructions and getting input
        # Get a selection from server
        print(instructions)
        serverChoice = input("Enter input > ")
        serverChoice = serverChoice.strip().lower()

        if serverChoice not in gameChoice:
            print("Please enter a valid choice: 'rock', 'paper', 'scissors'")
            serverChoice = input("Enter input > ")
            serverChoice = serverChoice.strip().lower()

        result = helper_validation(cleanClient, serverChoice)

        print(f"Client chose: {cleanClient}")
        if result == "draw":
            toClient = f"No one wins, it's a draw!\n"
        else:
            toClient = f"The winner this round is: {result}!\n"

        print(toClient)

        toClient += f"Server chose: {serverChoice}"
        connection_socket.send(toClient.encode())
        playingGame = False  # Resetting the flag

    elif cleanClient in gameChoice and playingGame is False:
        # Error, need to say play to play the game
        print(clientM)
        error = "Error, game must be initiated first by typing 'play'."
        print(error)
        connection_socket.send(error.encode())

    else:
        # Print message we got from client and then
        # get the input from the server to analyze.
        print(clientM)
        print("Type '/q' to terminate the connection.")
        serverM = input("Enter input > ")

        # Connection broke if 0 bytes are meant to be sent
        if serverM == "":
            print("Connection has broken.")
            break

        connection_socket.send(serverM.encode())

        cleanServer = serverM.strip().lower()
        if cleanServer == "/q":
            print("Bye bye!")
            break



connection_socket.close()
server_socket.close()

    # if clientM == "play":
    #     print(clientM)
    #     # We print the instructions and prompt a response
    #     print(instructions)
    #     serverM = input("Enter Input > ")
    #     connection_socket.send(serverM.encode())
    #
    # elif clientM == "/q":
    #     # Terminate the connection
    #     print("The client is terminating the connection. Bye bye!")
    #     connection_socket.close()
    #     break
    #
    # elif clientM in gameChoice and serverM != "":
    #     # Start playing
    #     # print(instructions)
    #     # serverM = input("Enter Input > ")
    #     result = helper_validation(clientM, serverM)
    #
    #     # print(f"Client chose: {clientM}")
    #
    #     if result == "draw":
    #         toClient = f"No one wins, it's a draw!\n"
    #     else:
    #         toClient = f"The winner this round is: {result}\n"
    #
    #     print(f"Client chose: {clientM}")
    #     print(toClient)
    #
    #     connection_socket.send(serverM.encode())
    #     continue
    #     # print("Waiting for server to reply...")
    #
    # else:
    #     print(clientM)
    #     serverM = input("Enter Input > ")
    #     serverM = serverM.strip().lower()
    #     if serverM == "/q":
    #         connection_socket.send(serverM.encode())
    #         print("Bye bye!")
    #         connection_socket.close()
    #         break
    #     else:
    #         connection_socket.send(serverM.encode())
    #         continue
