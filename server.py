# The functions of this server are:
# to be able to recieve a request from the controller for files
# to send file(s) to the controller after a request
# to receive one file at a time from the renderer
# to be able to stream and store files
# support text files (and maybe audio files if we have time)
import socket
from socket import *
import sys

serverPort = 1234

# function to launch the server


def launch():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # we need to control socket behavior, so add setsockopt method
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    print("Server initialized")

    # assign IP address and port number to this socket instance
    try:
        serverSocket.bind(('', serverPort))
        print("IP address assigned!")
    except error as errorMessage:
        print("Failed to assign IP address due to " + str(errorMessage))
        sys.exit()

    # TODO: should we have a value in the parameter to determine max connections?
    serverSocket.listen()
    print("waiting for requests. . .")

    while True:
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024)
            print("Recieved message: " + message)

            # CODE FOR FUNCTIONS OF THE SERVER

            # if requested for files to send to controller

            # if requested to send a file to renderer

            # if requested to end

            connectionSocket.close()
            print("connection closed")

        except IOError as errorMsg:
            print("Error " + str(errorMsg))
            # TODO: SEND THE ERROR MESSAGE TO THE CLIENT (CONTROLLER)


if __name__ == "__main__":
    launch()
