import socket
from tkinter import SEPARATOR
import nacl.utils
import nacl.secret

from nacl.signing import SigningKey
from nacl.signing import VerifyKey

from datetime import datetime

_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

USERS_INFO = {
    "admin" : "1234",
    "is705152@iteso.mx" : "5678"
}

f = open("serverLogs.txt", "w")

if __name__ == "__main__":
    BUFFER_SIZE = 4096

    host = "127.0.0.1"
    port = 65432

    SEPARATOR = "<SEPARATOR>"

    s = socket.socket()
    s.bind((host, port))
    s.listen()

    client_socket, address = s.accept()
    print(f"Conectado desde: {address}")

    allInfo = client_socket.recv(BUFFER_SIZE).decode()
    message, user, password, filename = allInfo.split(SEPARATOR)

    #Haciendo Login
    file = open("usersLog.txt", "a")

    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")

    if user != "" and password != "":
        if user in USERS_INFO and password in USERS_INFO.values():
            file.write(f"{currentTime}: El usuario {user} entro\n")
            file.write("\n")

            print("Encriptando archivo")
            box = nacl.secret.SecretBox(_key)
            encrypted = box.encrypt(bytes(message, 'utf-8'))
            f = open("serverLogs.txt", "a")
            f.write(f'Mensaje encriptado: \n {encrypted}\n')
            f.close()

            print("Desencriptando el archivo")
            box = nacl.secret.SecretBox(_key)
            decrypted = box.decrypt(encrypted)
            f = open("serverLogs.txt", "a")
            f.write(f'Mensaje desencriptado: \n{decrypted}\n')
            f.close()

            print("Firmar el archivo")
            sign_key = SigningKey.generate()
            signedFile = sign_key.sign(encrypted)
            f = open("serverLogs.txt", "a")
            f.write(f'Firma: \n{signedFile}\n')
            f.close()

            print("Verificar firma")
            verify_key = VerifyKey(sign_key.verify_key.encode())
            res = verify_key.verify(signedFile)

            f = open("serverLogs.txt", "a")
            f.write(f'Verificacion de firma: \n{res}\n')
            f.close()
    
    file.write(f"{currentTime}: El usuario {user} inento entrar\n")
    file.write("\n")
    file.close()

    s.close()