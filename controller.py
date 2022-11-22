# The functions of this controller are:
# to request files from the server
# to send a file to renderer to be rendered
# to be able to control the rendering e.g pause and resume the rendering

import socket
from socket import *
import sys


# function to fetch the files in the server
def requestFiles():
    # send message to server requesting to fetch files

    # parse the fetched data (could be multiple files so must make sure to account for that!)

    # store and print the files in a list

    return 0

# function to give the information to the renderer that it needs to get a file from the server


def sendToRenderer():
    # get the file name

    # send the name of that file to the renderer so that it knows which file to request from the server
    return 0

# function to create client to communicate with the host (server)


def createClient():
    # create socket for client

    # send the CORRECT type of message to the server

    # return/store the data recieved
    return 0

# function to close the client as well


def closeClient():

    return 0


if __name__ == "__main__":
    # run the functionality of the controller
    print("Hello World")
