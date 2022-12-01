import os


class Controller:
    Address = "10.0.0.1"


class Server:
    Port = 1234
    Address = "10.0.0.2"
    GET_FILES = 1


class Renderer:
    Port = 12345
    Address = "10.0.0.3"
    SEE_FILE_CONTENTS = 2


# global variable for the path of the directory the project is in
FILE_PATH = os.path.normpath("server_files")

EXIT_CODE = 3
ERROR_CODE = -1
