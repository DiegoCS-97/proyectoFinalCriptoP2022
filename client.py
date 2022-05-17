from fileinput import filename
import socket
from tkinter import SEPARATOR
from tkinter.filedialog import askopenfilename

BUFFER_SIZE = 4096

SEPARATOR = "<SEPARATOR>"

host = "127.0.0.1"
port = 65432

def login():
    print("Usuario: ")
    usuario = input(str())
    print("Contraseña: ")
    password = input(str())
    usuario_pass = [usuario, password]
    return usuario_pass

def openFile() -> str:
    filename = askopenfilename()
    return filename

if __name__ == "__main__":
    myCredentials = login()
    myFilePath = openFile()

    with open(myFilePath, 'rb') as fileDataToRead:
        message = fileDataToRead.read()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    s.sendall(f"{message}{SEPARATOR}{myCredentials[0]}{SEPARATOR}{myCredentials[1]}{SEPARATOR}{myCredentials}".encode())

    data = s.recv(BUFFER_SIZE)
    print(data.decode())