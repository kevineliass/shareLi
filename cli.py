from argparse import ArgumentParser
from pathlib import Path

def cli():
    parse = ArgumentParser(prog='ShareLi', description='Comparte archivos a otros dispositivos en la red local')
    parse.add_argument('file', type=Path, help='Archivo que se va a compartir')
    parse.add_argument('-s', '--server', type=str, help='Direccion ip hacia donde se enviara el archivo (ip explicita)')
    parse.add_argument('-p', '--port', type=int, default=15022, help='Puerto donde se ejecuta el servicio')
    return parse.parse_args()