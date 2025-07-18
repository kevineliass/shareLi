from sys import stdout, stderr

class Logger:
    def __init__(self, verbose=True):
        self.verbose = verbose
    
    def set_verbose(self, verbose):
        self.verbose = verbose
    
    def input(self, message=''):
        return input(message)
    
    def print(self, message='', file=stdout, end='\n'):
        if self.verbose:
            print(message, file=file, end=end)

    def log(self, message='', file=stdout, end='\n'):
        if self.verbose:
            print(f'[+] {message}', file=file, end=end)

    def warn(self, message='', file=stderr, end='\n'):
        print(f'[!] {message}', file=file, end=end)

    def err(self, message='', file=stderr, end='\n'):
        print(f'[-] {message}', file=file, end=end)
    
    def debug(self, message='', file=stdout, end='\n'):
        print(f'[DEBUG] {message}', file=file, end=end)


console = Logger()