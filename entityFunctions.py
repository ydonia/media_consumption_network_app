import os
import json


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

# we had a lot of trouble finding out how to read the json object after recieving it, we found a function in the link below
# https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # If this is a unicode string, return its string representation
    # if python 3, instead of below line use isinstance(data, str):
    if isinstance(data, unicode):
        return data.encode('utf-8')

    # If this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]

    # If this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # If it's anything else, return its original form
    return data
