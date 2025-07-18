from pathlib import Path
import socket
import random

class SocketManager:
    def __init__(self, socket_connection:socket.socket=None):
        self.socket_connection = socket_connection
        self.CHUNK = 1024 * 32
    
    def set_connection_socket(self, socket_connection_new):
        self.socket_connection = socket_connection_new

    def send(self, file:Path):
        filesize = file.stat().st_size # enviamos el tamaño del archivo para preparar que se reciba correctamente
        self.socket_connection.sendall(f'{filesize}\n'.encode())

        with file.open('rb') as f:
            data = f.read(self.CHUNK)
            while data:
                self.socket_connection.sendall(data)
                data = f.read(self.CHUNK)
        return True
    
    def recv(self):
        filesize = int(self.socket_connection.recv(32).decode().split('\n', 1)[0])
        file = Path(f'archivo_nuevo_{random.randint(1000, 9999)}.txt')
        file.touch()
        progress = 0

        with file.open('wb') as f:
            while progress < filesize:
                data = self.socket_connection.recv(self.CHUNK)
                if not data:
                    break
                f.write(data)
                progress += len(data)
        return True