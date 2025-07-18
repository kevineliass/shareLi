import socket
from logger import console
from shareLiError import ShareLiError
from socketManager import SocketManager
from pathlib import Path

HOST = '0.0.0.0'
PORT = 15022
HOSTNAME = 'eliaspc'

class ShareLiService(SocketManager): # servidor
    def __init__(self, socket_connection: socket.socket = None, file:Path = None):
        super().__init__(socket_connection)
        console.log('Listo para recibir archivos')
        super().recv(file)


def main(args=None):
    console.log('Iniciando servidor ShareLi...')
    with socket.socket() as s:
        s.bind( (HOST, PORT) )
        s.listen(5)
        console.log(f'Servidor ejecutandose en {HOST}:{PORT}')
        console.log('Esperando conexiones...')
        while True:
            conn, addr = s.accept()
            console.log(f'Conectado con: {addr}')
            cmd = conn.recv(1024)
            if cmd.decode() == 'available':
                console.debug('Enviando identificación')
                conn.sendall(HOSTNAME.encode())
            elif cmd.decode() == 'shareLi':
                console.log('Recibiendo archivo, enviando confirmacion')
                conn.sendall('ok'.encode())
                file = Path(conn.recv(1024).decode())
                conn.sendall('ok'.encode())
                shareli_service = ShareLiService(conn, file)
                console.log(f'Se guardo el archivo {file.name} con exito')
            else:
                console.debug('Comando desconocido!')



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.err('Programa interrumpido por el usuario!')
        exit(1)
    except ShareLiError as err:
        console.err(err)
        exit(1)