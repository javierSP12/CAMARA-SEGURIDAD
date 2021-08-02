# import the library
from appJar import gui
from PIL import Image, ImageTk
import numpy as np
import cv2
import registro
import conferencia
import threading
import socket
import CrearSocket
import queue
import time
import os

'''
* Clase: VideoClient
* ARGS_IN: object
* DESCRIPCIÓN: clase que se encarga de la parte visual de la práctica
* ARGS_OUT: Ninguno
'''
class VideoClient(object):
	'''
    * FUNCIÓN: __init__(self, window_size)
    * ARGS_IN: self: la propia clase, window_size: tamaño de la ventana de la aplicación
    * DESCRIPCIÓN: En está función inicializamos todos los parámetros que vamos a utilizar y creamos las diferentes
					ventanas que se van a utilizar
    * ARGS_OUT: Ninguno
    '''
	def __init__(self, window_size):
		
		# inicializamos todos los campos que vamos a necesitar como None
		self.PuertoTCP = "8000"
		self.nombreD = None
		self.puertoTCPD = None
		self.puertoUDPD = None
		self.direccionD = None
		self.direccion = None
		self.contrasena = None
		self.conexionControl = None
		self.incall = False
		self.pausa = False
		self.fin = False
		self.conferencia = None
		# Creamos una variable que contenga el GUI principal
		self.app = gui("Redes2 - P2P", window_size)
		self.app.setGuiPadding(10,10)

		# Preparación del interfaz
		self.app.addLabel("title", "Cliente Multimedia P2P - Redes2 ")
		self.app.addImage("video", "imgs/webcam.gif")

		# Registramos la función de captura de video
		# Esta misma función también sirve para enviar un vídeo
		self.cap = cv2.VideoCapture(0)
		VideoThread = threading.Thread(target=self.capturaVideo) # creamos el hilo que se va a encargar de capturar y enviar el video
		VideoThread.daemon = True 
		VideoThread.start()
		
		thread = threading.Thread(target=VideoClient.ControlServicio, args=(self,))
		thread.daemon = True
		thread.start()

	def start(self):
		self.app.go()
	def capturaVideo(self):
		num = 0
		# Mientras nos encontremos dentro de la aplicación
		while self.fin == False:
			# Capturamos un frame de la cámara o del vídeo
			ret, frame = self.cap.read()
			cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
			img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))

			# Lo mostramos en el GUI
			self.app.setImageSize("video", 640, 480)
			self.app.setImageData("video", img_tk, fmt = 'PhotoImage')

			# Si nos encontramos en una llamda y esta no se encuentra en pausa.
			if self.incall is not False:
				if self.pausa is False:
					num += 1
					# codificamos lo que hemos recibido del video o de la camara
					encode_param = [cv2.IMWRITE_JPEG_QUALITY,50]
					result,encimg = cv2.imencode('.jpg',frame ,encode_param)
					if result == False:
						print('Error al codificar imagen')
					# creamos la cabecera
					cabecera = str(num) + "#" + str(time.time()) + "#640x480" + "#10#"
					encimg = cabecera.encode() + encimg.tobytes()
					datos = encimg
					# enviamos la información codificada por el socket
					self.conferencia.sendVideo(datos)
		'''
	* FUNCIÓN: ControlServicio(self)
	* ARGS_IN: self: la propia clase
	* DESCRIPCIÓN: Controla las acciones para inicar, parar, recibir, cerrar una llamada
	* ARGS_OUT: Ninguno
	'''
	def ControlServicio(self):
		# Iniciamos el socket por el que vamos a hacer el control de la videollamada
		self.conexionControl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conexionControl.bind((self.direccion, int(self.PuertoTCP)))
		# mietras que no se vaya a cerrar la aplicación recibimos mensajes por el socket
		while self.fin is False:
			if self.conexionControl is not None:
				mensajeRes = ""
				self.conexionControl.listen(1)
				try:
					conn, addr = self.conexionControl.accept()
				except:
					return
				data = conn.recv(1440)
				# dividimos el mensaje que recibimos
				mensajeRes = data.decode().split(" ")
				# Si recibimos calling es que alguien nos está llamando
				if mensajeRes[0] == "CALLING":
					self.direccionD = mensajeRes[1]
					# Almacenamos su direccion, nombre y puerto UDP
					self.puertoUDPD = mensajeRes[2]
					
					# En el caso de que no nos encontremos en llamada
					if self.conferencia == None:
							self.conferencia = conferencia.llamada(self.direccion,self.direccionD, self.puertoTCPD, self.PuertoTCP)
					if self.incall == False:
						# Inciamos la clase conferenrencia y le establecemos el puerto UDP del usaurio destino
						self.conferencia.addUDPDestino(self.puertoUDPD)
					# Si nos encontramos en llamada devolvemos que nos encontramos ocupados
					else:
						self.conferencia.BusyCall()
				# Recibimos que se ha finalizado la llamada
				elif mensajeRes[0] == "CALL_END":
					self.incall = False
					# se cierra la ventana y los sockets y se muestra por pantalla
					self.app.hideSubWindow("RecibirImagen")
					self.app.warningBox("finalizada", "LLAMADA FINALIZADA")
					self.conferencia.cerrarSockects()
					self.conferencia = None
if __name__ == '__main__':

	vc = VideoClient("640x520")

	# Crear aquí los threads de lectura, de recepción y,
	# en general, todo el código de inicialización que sea necesario
	# ...


	# Lanza el bucle principal del GUI
	# El control ya NO vuelve de esta función, por lo que todas las
	# acciones deberán ser gestionadas desde callbacks y threads
	vc.start()
