from logger import console
from shareLiError import ShareLiError
from socketManager import SocketManager
from pathlib import Path
import socket

HOST = 'localhost'
PORT = 15022
FILE = Path('text.txt')

class ShareLiSend(SocketManager):
    def __init__(self, socket_connection: socket.socket = None):
        super().__init__(socket_connection)
    
    def send(self, file: Path):
        super().send(file)

def main(args=None):
    console.log(f'Conectando con {HOST}:{PORT}')
    with socket.socket() as s:
        s.connect( (HOST, PORT) )
        console.log(f'Enviando archivo {FILE.name}')
        shareli_send = ShareLiSend(s)
        shareli_send.send(FILE)
        console.log('Se envio el archivo correctamente.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.err('Programa interrumpido por el usuario!')
        exit(1)
    except ShareLiError as err:
        console.err(err)
        exit(1)