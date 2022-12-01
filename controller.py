# The functions of this controller are:
# to request files from the server
# to send a file to renderer to be rendered
# to be able to control the rendering e.g pause and resume the rendering

import socket
from socket import AF_INET, SOCK_STREAM
import sys
import json
from entityFunctions import Server, Controller, Renderer, EXIT_CODE


# function to send message based on the function and return the reponse to the message from the server or the renderer
def getResponse(option, message):
    # first, create socket to send message to the server
    controllerSocket = socket.socket(AF_INET, SOCK_STREAM)

    # carry out each function of the controller

    # if option 1 on the menu was chosen
    if option == Server.GET_FILES:
        controllerSocket.connect((Server.Address, Server.Port))
        controllerSocket.sendall(message)

    # if option 2
    elif option == Renderer.SEE_FILE_CONTENTS:
        controllerSocket.connect((Renderer.Address, Renderer.Port))
        controllerSocket.sendall(message)

    # if option 3
    elif option == Server.EXIT:

        # send exit code to server to terminate the program
        controllerSocket.connect((Server.Address, Server.Port))
        controllerSocket.sendall(message)
        controllerSocket.close()

        # do the same with the renderer
        controllerSocket = socket.socket(AF_INET, SOCK_STREAM)
        controllerSocket.connect((Renderer.Address, Renderer.Port))
        controllerSocket.sendall(message)

    response = controllerSocket.recv(1024)
    print("response from server: " + str(response))
    controllerSocket.close()
    return response


# function to fetch the files in the server
def getFiles():
    # send message to server requesting to fetch files using JSON
    # (using dumps, not dump because we don't want to create a file every time we use the method: https://www.analyticssteps.com/blogs/working-python-json-object)
    message = json.dumps({"function": Server.GET_FILES})
    response = getResponse(Server.GET_FILES, message).decode()
    response = json.loads(response)  # convert to json object?
    # TODO: encoding and decoding

    # decode and parse the fetched data (could be multiple files so must make sure to account for that!)
    fileList = response["data"]

    # store and print the files in a list
    print("Files contained in Server:\n" + str(fileList))


# function to give the information to the renderer that it needs to get a file from the server
def seeFileContents():
    # get the file name
    fileName = input("Enter the name of the file you would like to render: ")

    # send the name of that file to the renderer so that it knows which file to request from the server
    message = {}
    message["function"] = Renderer.SEE_FILE_CONTENTS
    message["data"] = fileName
    # turn the dictionary into a json file. easiest to parse
    message = json.dumps(message)

    response = getResponse(Renderer.SEE_FILE_CONTENTS, message)
    print("response from Renderer: " + str(response))


# function to display the options to the user
def displayOptions():
    menu = (
        "Welcome to your Media Consumption Service! \n"
        "Choose one of the options below.\n"
        "1. Display files in the Server\n"
        "2. See the contents of a specific file\n"
        "3. Exit app\n"
    )
    validChoice = False
    while not validChoice:
        choice = input(menu)
        choice = int(choice)
        if (choice < 1) or (choice > 3):
            print("Please pick a number between 1 and 3. Try again.")
        else:  # if valid option
            validChoice = True
    return choice


# send the shutdown signal to the server
def send_shutdown_signal():
    message = {}
    message["function"] = EXIT_CODE
    message = json.dumps(message)

    response = getResponse(EXIT_CODE, message).decode()
    exitMessage = response["data"]
    print("Shutdown response: " + str(exitMessage))
    print("Exiting app.")
    sys.exit()


# main function to run the controller
def run():
    exiting = False
    while not exiting:
        option = displayOptions()

        # get files from Server
        if option == 1:
            getFiles()
        elif option == 2:
            seeFileContents()
        elif option == 3:
            exiting = True
            send_shutdown_signal()


if __name__ == "__main__":
    option = displayOptions()

    run()
