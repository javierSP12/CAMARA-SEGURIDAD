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
		self.nombre = None
		self.PuertoTCP = None
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
		
	def start(self):
		self.app.go()
def recibirVideo(self):
		# Mostramos la subventana de recibir imagen
		self.app.showSubWindow("RecibirImagen")
		# Mientras que nos encontremos en una llamada y está no esté en pausa
		# extraemos los elementos del buffer (cola) y los convertimos en imagenes
		while self.incall == True:
			if self.pausa is False:
				if self.conferencia.queue.empty() == True:
					continue
				encimg = self.conferencia.queue.get()
				decimg = cv2.imdecode(np.frombuffer(encimg,np.uint8), 1)
				# Conversión de formato para su uso en el GUI
				cv2_im = cv2.cvtColor(decimg,cv2.COLOR_BGR2RGB)
				img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))
				self.app.setImageSize("VideoR", 640, 480)
				self.app.setImageData("VideoR", img_tk, fmt = 'PhotoImage')

if __name__ == '__main__':

	vc = VideoClient("640x520")

	# Crear aquí los threads de lectura, de recepción y,
	# en general, todo el código de inicialización que sea necesario
	# ...


	# Lanza el bucle principal del GUI
	# El control ya NO vuelve de esta función, por lo que todas las
	# acciones deberán ser gestionadas desde callbacks y threads
	vc.start()
