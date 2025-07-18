from logger import console
from shareLiError import ShareLiError
from socketManager import SocketManager
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from cli import cli
import ipaddress
import socket

NETMASK = '192.168.100.0/24'
TIMEOUT = 0.5

class ShareLiSend(SocketManager):
    def __init__(self, socket_connection: socket.socket = None):
        super().__init__(socket_connection)
    
    def send(self, file: Path):
        super().send(file)

def scan_host(ip):
    try:
        with socket.socket() as s:
            s.settimeout(TIMEOUT)
            s.connect( (ip, args.port) )
            s.sendall('available'.encode())
            hostname = s.recv(1024).decode()
            return {'address': ip, 'hostname':hostname}
    except:
        return None

def find_servers():
    hosts = list(ipaddress.IPv4Network(NETMASK).hosts())
    hosts.append('localhost')
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_host, ip) for ip in hosts]
        servers = [future.result() for future in futures if future.result()]
    return servers

def main(args=None):
    if not args.server:
        console.log('Buscando servidores disponibles...')
        servers = find_servers()
        for server in servers:
            console.print(f'{server["address"]}:{server["hostname"]}')
        console.log('Vuelve a ejecutar con la opcion "--server" usando una direccion ip')
        exit(0)
    
    server = scan_host(args.server)
    if not server:
        raise ShareLiError('La direccion ip no es valida!')

    console.log(f'Conectado con {server["hostname"]}')
    console.log('Comenzando el envio del archivo...')
    with socket.socket() as s:
        s.connect( (server["address"], args.port) )
        s.sendall('shareLi'.encode()) # comando para preparar recibo en el servidor
        if not s.recv(1024).decode() == 'ok':
            raise ShareLiError('El servidor no puede recibir archivos en este momento')
        s.sendall(f'{args.file.name}'.encode()) # nombre del archivo hacia el servidor
        if not s.recv(1024).decode() == 'ok':
            raise ShareLiError('Ocurrio un error inesperado')
        shareli_send = ShareLiSend(s)
        shareli_send.send(args.file)
        console.log('Se envio el archivo correctamente.')


if __name__ == '__main__':
    try:
        global args
        args = cli()
        main(args)
    except KeyboardInterrupt:
        console.err('Programa interrumpido por el usuario!')
        exit(1)
    except ShareLiError as err:
        console.err(err)
        exit(1)