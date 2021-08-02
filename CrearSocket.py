import socket

'''
* FUNCIÓN: crearSocket()
* ARGS_IN: Ninguno
* DESCRIPCIÓN: En esta funcion se crea el socket necesario para contactar con el servidor de descubrimiento
* ARGS_OUT: regSocket: socket que se va a utilizar con el servidor de descubrimiento
'''
def crearSocket():
    regSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    regSocket.connect(("vega.ii.uam.es", 8000))
    return regSocket

'''
* FUNCIÓN: crearSocketTCPControl()
* ARGS_IN: ip y puerto en el que tendremos que inicializar el socket
* DESCRIPCIÓN: En esta funcion se crea el socket necesario para llevar a cabo el control de la llamada
* ARGS_OUT: sock: socket que se va a utilizar en el control de la llamada
'''
def crearSocketTCPControl(ip, puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, puerto))
    return sock
