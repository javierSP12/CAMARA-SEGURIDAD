import socket
import CrearSocket
import queue
import numpy as np

'''
* Clase: llamada
* ARGS_IN: Ninguno
* DESCRIPCIÓN: clase que se encarga de controlar toda la llamada entre los dos usuarios
* ARGS_OUT: Ninguno
'''
class llamada:
    '''
    * FUNCIÓN: __init__(self, ip,nickDest, nickUsuario,ipDest, puertoDest, puertoUsuario)
    * ARGS_IN: self: la propia clase, ip: ip propia, nickDest: nombre del usuario al que se quiere llamar,
                    ipDest: ip del usuario al que se quiere llamar, puertoDest: puerto del usuario al que se quiere llamar
    * DESCRIPCIÓN: En esta funcion se almacenan en la clase los paramentros de entrada pasados como argumento
    * ARGS_OUT: Ninguno
    '''
    def __init__(self, ip,nickDest, nickUsuario,ipDest, puertoDest, puertoUsuario):
        # guardar los parametros de entrada en clase
        self.myIP = ip
        self.myNick = nickUsuario
        self.myPuertoUDP=0 
        self.ipDest=ipDest
        self.nickDest=nickDest
        self.puertoDTCP=puertoDest
        self.DestPuertoUDP = 0
        self.puertoDUDP = 0
        # Inicializa a None los diferentes sockets que van a ser utilizados
        self.conexionControl = None
        self.videoSocketSend = None
        self.videoSocketRec = None
        # inicializa la cola que nos servirá como buffer
        self.queue = queue.Queue(40)
        self.fin = False
   
    '''
    * FUNCIÓN: InicioLlamada(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario que se quiere llamar el inicio de llamada
    * ARGS_OUT: Ninguno
    '''

    def InicioLlamada(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info 
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP)) 
        mensaje = "CALLING " + self.myNick + " " + "6000"
        self.myPuertoUDP = 6000 # guardamos el puerto UDP que va a utilizar el usuario llamante
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de CALLING por el socket
        self.conexionControl.close() # cerramos el socket

    '''
    * FUNCIÓN: AcceptCall(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario que se ha aceptado la llamada
    * ARGS_OUT: Ninguno
    '''
    def AcceptCall(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info 
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP))
        mensaje = "CALL_ACCEPTED " + self.myNick + " " + "5100"
        self.myPuertoUDP = 5100 # guardamos el puerto UDP que va a utilizar el usuario llamante
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de CALL_ACCEPTED por el socket
        self.conexionControl.close() # cerramos el socket
        return

    '''
    * FUNCIÓN: DenieCall(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario que se ha rechazado la llamada
    * ARGS_OUT: Ninguno
    '''
    def DenieCall(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info 
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP))
        mensaje = "CALL_DENIED " + self.myNick
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de CALL_DENIED por el socket
        self.conexionControl.close() # cerramos el socket
        return
    '''
    * FUNCIÓN: HoldCall(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario que se ha pausado la llamada
    * ARGS_OUT: Ninguno
    '''
    def HoldCall(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info 
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP))
        mensaje = "CALL_HOLD " + self.myNick
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de CALL_HOLD por el socket
        self.conexionControl.close() # cerramos el socket
        return
    '''
    * FUNCIÓN: ResumeCall(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario que se ha retomado la llamada
    * ARGS_OUT: Ninguno
    '''
    def ResumeCall(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP))
        mensaje = "CALL_RESUME " + self.myNick
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de CALL_RESUME por el socket
        self.conexionControl.close() # cerramos el socket
        return
    '''
    * FUNCIÓN: EndCall(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario que se ha finalizado la llamada
    * ARGS_OUT: Ninguno
    '''
    def EndCall(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP))
        mensaje = "CALL_END " + self.myNick
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de CALL_END por el socket
        self.conexionControl.close() # cerramos el socket
        return
    '''
    * FUNCIÓN: BusyCall(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta funcion se envía por el socket al usuario se encuentra ocupado en otra llamada
    * ARGS_OUT: Ninguno
    '''
    def BusyCall(self):
        # Creamos el socket para la ip y puerto del usuario destino para poder enviarle la info
        self.conexionControl = CrearSocket.crearSocketTCPControl(self.ipDest, int(self.puertoDTCP))
        mensaje = "CALL_BUSY " + self.myNick
        men = mensaje.encode()
        self.conexionControl.send(men) # enviamos el mensaje de BUSY por el socket
        self.conexionControl.close() # cerramos el socket
        return

    '''
    * FUNCIÓN: CrearLlamada(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta función se crea el socket UDP que utilizaremos para enviar los paquetes
    * ARGS_OUT: Ninguno
    '''
    def CrearLlamada(self):
        # Creamos el socket UDP que servirá para enviar los paquetes
        self.videoSocketSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    '''
    * FUNCIÓN: SendVideo(self)
    * ARGS_IN: self: la propia clase, video: Paquetes video a enviar
    * DESCRIPCIÓN: En esta función se enviarán los paquetes del video
    * ARGS_OUT: Ninguno
    '''
    def sendVideo(self, video):
        # Enviamos a través del socket la información a la ip y puerto del usuario destino
        self.videoSocketSend.sendto(video, (self.ipDest,self.DestPuertoUDP))

    '''
    * FUNCIÓN: RecvVideo(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: En esta función se recibirán los paquetes del video
    * ARGS_OUT: Ninguno
    '''
    def RecVideo(self):
        # Creamos el socket UDP que servirá para recibir los paquetes
        self.videoSocketRec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.videoSocketRec.bind((self.myIP, self.myPuertoUDP))
        # Mientras no se haya terminado la llamda seguiremos esperando paquetes
        while self.fin is False:
            try:
                data, address = self.videoSocketRec.recvfrom(65535) # recibimos los paquetes
                # separamos el paquete de su cabecera y lo metemos en la cola (buffer de recepción)
                datos = data.split(b"#", 4)
                encimg = np.fromstring(datos[4], dtype=np.uint8)
                self.queue.put(encimg)
            except:
                return

    '''
    * FUNCIÓN: addUDPDestino(self)
    * ARGS_IN: self: la propia clase, puertoUDP: puerto UDP que utiliza el usario de destino 
    * DESCRIPCIÓN: añadimos a la clase el puerto UDP del usuario de destino
    * ARGS_OUT: Ninguno
    '''
    def addUDPDestino(self, puertoUDP):
        self.DestPuertoUDP = int(puertoUDP)
        return
    '''
    * FUNCIÓN: cerrarSockects(self)
    * ARGS_IN: self: la propia clase
    * DESCRIPCIÓN: función para cerrar los sockets utilizados para el envio y recepción del video
    * ARGS_OUT: Ninguno
    '''
    def cerrarSockects(self):
        self.fin = True
        self.videoSocketRec.close()
        self.videoSocketSend.close()
        return
