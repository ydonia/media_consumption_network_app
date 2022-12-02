# The functions of this server are:
# to be able to recieve a request from the controller for files
# to send file(s) to the controller after a request
# to receive one file at a time from the renderer
# to be able to stream and store files
# support text files (and maybe audio files if we have time)
import socket
from socket import *
from os import *
from os.path import isfile, join
import sys
import json
from entityFunctions import Server, Controller, Renderer, EXIT_CODE, ERROR_CODE
from entityFunctions import FILE_PATH
from entityFunctions import json_loads_byteified

# function to launch the server


def launch():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # we need to control socket behavior, so add setsockopt method
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    print("Server initialized")

    # assign IP address and port number to this socket instance
    try:
        serverSocket.bind(('', Server.Port))
        print("Server port assigned!")
    except error as errorMessage:
        print("Failed to assign IP address due to " + str(errorMessage))
        sys.exit()

    # Get the server to listen, 2 connections max, the controller and renderer
    serverSocket.listen(2)
    print("waiting for requests. . .")

    while True:
        connectionSocket, address = serverSocket.accept()
        if address == Controller.Address:
            print("recieving message from Controller at: " + str(address))
        elif address == Renderer.Address:
            print("recieving message from Renderer at: " + str(address))
        else:
            print("recieving message from address: " + str(address))

        # recieve the message (and decode + convert to json)
        # from the client and give a reponse depending on what the client is asking
        try:
            message = json_loads_byteified(connectionSocket.recv(1024))
            # print("Recieved message of type: " + type(message))

            # get value from key in dictionary
            option = message.get("function")

            # CODE FOR FUNCTIONS OF THE SERVER

            if option == Server.GET_FILES:
                # gather the names of all the files in the server and send to controller
                files = [file for file in listdir(
                    FILE_PATH) if isfile(join(FILE_PATH, file))]
                response = json.dumps({"data": files})
                connectionSocket.sendall(response)
                # TODO: not sure if above encoding is correct

            # if requested to send a file to renderer
            elif option == Renderer.SEE_FILE_CONTENTS:
                path = join(FILE_PATH, message.get("data"))
                file = open(path, "rb")
                responseMessage = {}
                responseMessage["function"] == Renderer.SEE_FILE_CONTENTS
                responseMessage["file_name"] = message.get("data")
                responseMessage["data"] = file.read()

                response = json.dumps(responseMessage)
                connectionSocket.sendall(response)

            # if requested to end
            elif option == EXIT_CODE:
                response = json.dumps({"data": "closing server program"})
                connectionSocket.sendall(response)
                # TODO: encoding
                break

            connectionSocket.close()
            print("connection closed")

        except IOError as errorMsg:
            print("Error " + str(errorMsg))
            # TODO: SEND THE ERROR MESSAGE TO THE CLIENT (CONTROLLER)
            response = {}
            response["function"] = ERROR_CODE
            response["data"] = "File " + message.get("data") + " not found"
            connectionSocket.sendall(json.dumps(response))
            connectionSocket.close()

    print("Shutting down server.")
    serverSocket.shutdown(SHUT_RDWR)
    serverSocket.close()


if __name__ == "__main__":
    launch()
