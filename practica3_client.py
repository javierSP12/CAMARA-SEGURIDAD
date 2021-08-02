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
		VideoThread.start() # Iniciamos el hilo
		# Añadir los botones
		self.app.addButtons(["Conectar", "SeleccionarVideo", "Salir"], self.buttonsCallback)
		# Creamos la subventana que nos va a permitir conectar con otro usuario para iniciar la llamada
		self.app.startSubWindow("Conectar", modal=True)
		self.app.setPadding(10,10)

		# Introducimos el usuario
		self.app.addLabelEntry("UsuarioLlamar")

		# creamos los Botones
		self.app.addButtons(["conectar", "volver"], self.buttonsCallback)

		self.app.stopSubWindow()
		# Creamos la subventana que se va a abrir cuando recibamos una llamada para aceptarla o rechazarla
		self.app.startSubWindow("RecibiendoLlamada", modal=True)
		self.app.setPadding(10,10)
		# Titulo de la subventana
		self.app.addLabel("title1", "Llamada Entrante")
		# Botones
		self.app.addButtons(["aceptar", "rechazar"], self.buttonsCallback)

		self.app.stopSubWindow()
		# Creamos la subventana que se va a abrir para llevar a cabo el registro en la aplicacion
		self.app.startSubWindow("Register", modal=True)
		self.app.setPadding(10,10)

		# Todos los campos que serán necesario cumplimentar para registro
		self.app.addLabelEntry("NickRegister")
		self.app.addLabelSecretEntry("PassRegister")
		self.app.addLabelEntry("IP")
		self.app.addLabelEntry("Puerto")
		# Botones
		self.app.addButtons(["Registrar", "CancelarRegistro"], self.buttonsCallback)

		self.app.stopSubWindow()
		# Creamos la subventana que se va a abrir cuando nos encontremos dentro de una videoLlamada
		self.app.startSubWindow("RecibirImagen")
		self.app.addImage("VideoR", "imgs/webcam.gif", 1, 2, 5, 5)
		# botones
		self.app.addButtons(["Pausar", "Reanudar", "Colgar"], self.buttonsCallback)
		self.app.stopSubWindow()
		self.app.hideSubWindow("RecibirImagen")
	'''
	* FUNCIÓN: start(self)
	* ARGS_IN: self: la propia clase
	* DESCRIPCIÓN: En está función se va proceder a abrir la interfaz gráfica con la subventana de registro
	* ARGS_OUT: Ninguno
	'''
	def start(self):
		self.app.go(startWindow="Register")
	'''
	* FUNCIÓN: recibirVideo(self)
	* ARGS_IN: self: la propia clase
	* DESCRIPCIÓN: En está función se va recibir el video que nos han enviado por la videollamada y mostrarlo por pantalla
	* ARGS_OUT: Ninguno
	'''
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
			
	'''
	* FUNCIÓN: capturaVideo(self)
	* ARGS_IN: self: la propia clase
	* DESCRIPCIÓN: En está función se va a encargar de capturar el video y de enviarlo
	* ARGS_OUT: Ninguno
	'''
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
	* FUNCIÓN: setImageResolution(self, resolution)
	* ARGS_IN: self: la propia clase, resolution: resolución que va a tener el video
	* DESCRIPCIÓN: Se establece la resolución de captura de la webcam
	* ARGS_OUT: Ninguno
	'''
	def setImageResolution(self, resolution):
		# Se establece la resolución de captura de la webcam
		# Puede añadirse algún valor superior si la cámara lo permite
		# pero no modificar estos
		if resolution == "LOW":
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
		elif resolution == "MEDIUM":
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
		elif resolution == "HIGH":
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	'''
	* FUNCIÓN: buttonsCallback(self, button)
	* ARGS_IN: self: la propia clase, button: nombre del botón pulsado
	* DESCRIPCIÓN: Controla las acciones que se van a realizar al pulsar un boton
	* ARGS_OUT: Ninguno
	'''
	def buttonsCallback(self, button):

		if button == "Salir":
			# Salimos de la aplicación, cerramos la conexión de control y marcamos el fin
			self.conexionControl.close()
			self.fin = True
			self.app.stop()
		elif button == "Conectar":
			# Mostramos la subventana que nos permitirá introducir el nick del usuario con 
			# el que queremos conectar
			self.app.hideSubWindow("Register")
			self.app.hideSubWindow("RecibiendoLlamada")
			self.app.showSubWindow("Conectar")
		elif button == "conectar":
			# obtenemos el nick del usuario que hemos introducido
			self.nombreD = self.app.getEntry("UsuarioLlamar")
			# si está vacio mostramos el error
			if self.nombreD == "":
				self.app.warningBox("Error", "Rellene todo los campos", parent="Conectar")
				self.app.clearAllEntries()
			# Si no está vacio buscamos en el servidor de descubrimiento
			else:
				query = registro.query(self.nombreD)
				# Si no encuentra el usuario lo muestra por pantalla
				if query == "Usuario no encontrado":
					self.app.warningBox("Error", "Usuario No encontrado", parent="Conectar")
					self.app.clearAllEntries()
				# Si encuentra el usuario Iniciamos la llamada
				else:
					queryS = query.split(" ")
					self.direccionD = queryS[1]
					self.puertoTCPD = queryS[2]
					if self.conferencia == None:
						self.conferencia = conferencia.llamada(self.direccion,self.nombreD, self.nombre,self.direccionD, self.puertoTCPD, self.PuertoTCP)
					self.conferencia.InicioLlamada()
			self.app.hideSubWindow("Conectar")
			self.app.show() # Volvemos a mostrar la pantalla pricipal
		elif button == "aceptar":
			# Llamamos a aceptar llamada y creamos la llamada
			self.app.hideSubWindow("Register")
			self.app.hideSubWindow("Conectar")
			if self.conferencia == None:
				self.conferencia = conferencia.llamada(self.direccion,self.nombreD, self.nombre,self.direccionD, self.puertoTCPD, self.PuertoTCP)	
			self.conferencia.AcceptCall()
			self.conferencia.CrearLlamada()
			
			self.app.hideSubWindow("RecibiendoLlamada") # Mostramos la pantalla principal de nuevo
			self.incall = True
			RecVideo = threading.Thread(target=self.conferencia.RecVideo) # inicializamos el hilo que recibirá los datos y los mete en el buffer
			recibirVideo = threading.Thread(target=self.recibirVideo) # inicializamos el hilo que nos mostrará las imagenes en la subventana
			# Lanza los hilos
			RecVideo.start()
			time.sleep(1)
			recibirVideo.start()
			self.app.show()
			
		elif button == "rechazar":
			# Llamamos a rechazar la llamada y volvemos a la ventana principal
			if self.conferencia == None:
				self.conferencia = conferencia.llamada(self.direccion,self.nombreD, self.nombre,self.direccionD, self.puertoTCPD, self.PuertoTCP)	
			self.conferencia.DenieCall()
			self.app.hideSubWindow("RecibiendoLlamada")
			self.app.show()
		elif button == "volver":
			# cerramos la pantalla conectar y volvemos a la principal
			self.app.hideSubWindow("Conectar")
			self.app.show()

		elif button == "CancelarRegistro":
			# cerramos la aplicación trás cancelar el registro
			self.app.stop()
		elif button == "Colgar":
			# Establecemos que ya no estamos en llamada y cerramos la ventana de recibir imagen
			self.incall = False
			self.app.hideSubWindow("RecibirImagen")
			# Llamamos a End Call y cerramos los sockets UDP
			self.conferencia.EndCall()
			self.conferencia.cerrarSockects()
		elif button == "Pausar":
			# Ponemos en pausa la llamada
			if self.pausa is False:
				self.pausa = True
				self.conferencia.HoldCall()
		elif button == "Reanudar":
			# Reanudamos la llamda
			self.pausa = False
			self.conferencia.ResumeCall()
		elif button == "Registrar":
			# Procedemos a registrar usuario cogiendo todos los campos
			self.nombre = self.app.getEntry("NickRegister")
			self.direccion = self.app.getEntry("IP")
			self.PuertoTCP = self.app.getEntry("Puerto")
			self.contrasena = self.app.getEntry("PassRegister")
			# Si algún campo está vacio mostrar error
			if self.contrasena == "" or self.nombre == "" or self.PuertoTCP == "" or self.direccion == "":
				self.app.warningBox("Error", "Rellene todo los campos", parent="Register")
				self.app.clearAllEntries()
			# Si registro incorrecto mostrar error
			mensaje = registro.registrar(self.nombre, self.direccion, self.PuertoTCP, self.contrasena, "V0")
			if mensaje == "Registro Incorrecto":
				self.app.warningBox("Error", "Registro Incorrecto", parent="Register")
				self.app.clearAllEntries()
			# Si registro correcto mostrar la pantalla principal e iniciar el hilo que contiene el control de la llamada
			else:
				self.app.hideSubWindow("Register")
				self.app.show()
				thread = threading.Thread(target=VideoClient.ControlServicio, args=(self,))
				thread.daemon = True
				thread.start()
		# Botón que permite seleccionar un video para que sea mostrado en vez de la webcam, puede ser formato divx, avi, mp4 o mov
		elif button == "SeleccionarVideo":
			filename = self.app.openBox(title="Directorio", dirName=os.getcwd(), fileTypes=[('video', '*.divx'), ('video', '*.avi'), ('video', '*.mp4'), ('video', '*.mov')], asFile=False, parent=None)
			self.cap = cv2.VideoCapture(filename)

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
					self.nombreD = mensajeRes[1]
					reg = registro.query(self.nombreD).split(" ") # buscamos su información en el servidor de descubrimiento
					# Almacenamos su direccion, nombre y puerto UDP
					self.direccionD = reg[1]
					self.nomreD = mensajeRes[1]
					self.puertoUDPD = mensajeRes[2]
					query = registro.query(self.nombreD).split(" ")
					self.direccionD = query[1]
					self.puertoTCPD = query[2]
					# En el caso de que no nos encontremos en llamada
					if self.conferencia == None:
							self.conferencia = conferencia.llamada(self.direccion,self.nombreD, self.nombre,self.direccionD, self.puertoTCPD, self.PuertoTCP)
					if self.incall == False:
						# Inciamos la clase conferenrencia y le establecemos el puerto UDP del usaurio destino
						self.conferencia.addUDPDestino(self.puertoUDPD)
						self.app.hideSubWindow("Register")
						self.app.hideSubWindow("Conectar")
						self.app.showSubWindow("RecibiendoLlamada")
					# Si nos encontramos en llamada devolvemos que nos encontramos ocupados
					else:
						self.conferencia.BusyCall()
				# Si recibimos que nuetra llamada ha sido aceptada
				elif mensajeRes[0] == "CALL_ACCEPTED":
					# Creamos la clase conferencia, añadimos el puerto UDP y creamos la llamada
					self.puertoUDPD = mensajeRes[2]
					
					if self.conferencia == None:
						self.conferencia = conferencia.llamada(self.direccion,self.nombreD, self.nombre,self.direccionD, self.puertoTCPD, self.PuertoTCP)
					self.conferencia.addUDPDestino(mensajeRes[2])
					self.conferencia.CrearLlamada()
					# Creamos los hilos destinados a recibir los paquetes y meterlas en buffer y el que lee el buffer y convierte los paquetes en imagenes 
					self.incall = True
					RecVideo = threading.Thread(target=self.conferencia.RecVideo)
					recibirVideo = threading.Thread(target=self.recibirVideo)
					# Lanza los hilos
					RecVideo.start()
					time.sleep(1)
					recibirVideo.start()
					self.app.show()
				# Recibimos que se ha rechazado la llamada
				elif mensajeRes[0] == "CALL_DENIED":
					# lo mostramos por pantalla
					self.app.warningBox("rechazada", "LLAMADA RECHAZADA")
				# Recibimos que se ha vuelto la llamada
				elif mensajeRes[0] == "CALL_RESUME":
					self.pause = False
					# lo mostramos por pantalla
					self.app.warningBox("Resume", "LLAMADA EN RETOMADA")
				# Recibimos que se ha finalizado la llamada
				elif mensajeRes[0] == "CALL_END":
					self.incall = False
					# se cierra la ventana y los sockets y se muestra por pantalla
					self.app.hideSubWindow("RecibirImagen")
					self.app.warningBox("finalizada", "LLAMADA FINALIZADA")
					self.conferencia.cerrarSockects()
					self.conferencia = None
				# Recibimos que se ha parado la llamada
				elif mensajeRes[0] == "CALL_HOLD":
					# lo mostramos por pantalla
					self.app.warningBox("espera", "LLAMADA EN ESPERA")
					self.pause = True
				# Recibimos que el otro usuario está ocupado
				elif mensajeRes[0] == "CALL_BUSY":
					# lo mostramos por pantalla
					self.app.warningBox("busy", "El usuario está ocupado")




if __name__ == '__main__':

	vc = VideoClient("640x520")

	# Crear aquí los threads de lectura, de recepción y,
	# en general, todo el código de inicialización que sea necesario
	# ...


	# Lanza el bucle principal del GUI
	# El control ya NO vuelve de esta función, por lo que todas las
	# acciones deberán ser gestionadas desde callbacks y threads
	vc.start()
