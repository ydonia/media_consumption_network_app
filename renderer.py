# This renderer's function is:
# to successfully recieve a file from the controller
# to render that file
# to send that file to the server to be streamed
import json
import socket
import sys
import entityFunctions
from entityFunctions import *


def rendererStart():
    rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Created the Render Socket")

    try:
        rSocket.bind((Renderer.Address, Renderer.Port))
        print("Bind complete")
        print("Renderer Address: ", rSocket.getsockname())

    except socket.error:
        print("Binding Error, exiting program...")
        sys.exit()

    rSocket.listen(2)

    enabled = True
    while enabled:
        connection, address = rSocket.accept()
        print("incoming address: " + str(address))

        try:
            message = connection.recv(1024)
            print(str(message))
            message = entityFunctions.json_loads_byteified(message)
            messageType = message.get("function")

            if messageType is Renderer.SEE_FILE_CONTENTS:
                payload = json.dumps(message)

                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((Server.Address, Server.Port))
                client.sendall(payload)

                payload = client.recv(2048)
                payload = entityFunctions.json_loads_byteified(payload)

                if payload["function"] is ERROR_CODE:
                    print(payload["data"])
                else:
                    print("File: " + payload["file_name"])
                    print(payload["data"])

            elif messageType is EXIT_CODE:
                enabled = False
                data = json.dumps({"data": "[RENDERER] shutting down"})
                connection.sendall(data)

            print("Connection closing...")
            client.close()
            connection.close()

        except IOError as e:
            print(str(e))
            connection.close()
    rSocket.shutdown()
    rSocket.close()
    print("Program Closing...")


rendererStart()
