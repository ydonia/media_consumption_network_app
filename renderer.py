# This renderer's function is:
# to successfully recieve a file from the controller
# to render that file
# to send that file to the server to be streamed
from cgitb import enable
from email import message
import json
from pydoc import cli
from utils import Addresses, MessageTypes, Ports
import socket
import sys
import utils
from utils import *

def rendererStart():
    print("runs")
    renderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    renderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Created the Render Socket")

    try:
        renderSocket.bind("", Ports.RENDERER)
        print("Bind complete")


    except socket.error:
        print("Binding Error, exiting program...")
        sys.exit()

    renderSocket.listen(2)

    enabled = True
    while enabled:
        connection, address = renderSocket.accept()
        print("incoming address: " + str(address))

        try:
            message = connection.recv(1024)
            print(str(message))
            message = utils.json_loads_byteified(message)
            messageType = message.get("type")

            if messageType is MessageTypes.REQUEST:
                payload = json.dumps(message)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((Addresses.SERVER, Ports.SERVER))
                client.sendall(payload)
                payload = client.recv(2048)

                payload = utils.json_loads_byteified(payload)

                if payload["type"] is MessageTypes.ERROR:
                    print(payload["content"])
                else:
                    print("File: " + payload["fileName"])
                    print(payload["content"])
            
            elif messageType is MessageTypes.EXIT:
                enabled = False
                data = json.dumps({"content": "[RENDERER] shutting down"})
                connection.sendall(data)



            print("Connection closing...")
            client.close()    
            connection.close()

        except IOError as e:
            print(str(e))
            connection.close()
    renderSocket.shutdown()
    renderSocket.close()
    print("Program Closing...")


rendererStart()