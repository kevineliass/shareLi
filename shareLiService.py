import socket
from logger import console
from shareLiError import ShareLiError
from socketManager import SocketManager

HOST = 'localhost'
PORT = 15022

class ShareLiService(SocketManager): # servidor
    def __init__(self, socket_connection: socket.socket = None):
        super().__init__(socket_connection)
        console.log('Listo para recibir archivos')
        super().recv()


def main(args=None):
    console.log('Iniciando servidor ShareLi...')
    with socket.socket() as s:
        s.bind( (HOST, PORT) )
        s.listen(1)
        console.log(f'Servidor ejecutandose en {HOST}:{PORT}')
        console.log('Esperando conexiones...')
        conn, addr = s.accept()
        console.log(f'Conectado con: {addr}')
        shareli_service = ShareLiService(conn)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.err('Programa interrumpido por el usuario!')
        exit(1)
    except ShareLiError as err:
        console.err(err)
        exit(1)