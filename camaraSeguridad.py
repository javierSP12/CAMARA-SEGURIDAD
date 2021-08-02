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

if __name__ == '__main__':

	vc = VideoClient("640x520")

	# Crear aquí los threads de lectura, de recepción y,
	# en general, todo el código de inicialización que sea necesario
	# ...


	# Lanza el bucle principal del GUI
	# El control ya NO vuelve de esta función, por lo que todas las
	# acciones deberán ser gestionadas desde callbacks y threads
	vc.start()
