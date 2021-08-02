import socket
import CrearSocket
import sys
from importlib import reload
'''
* FUNCIÓN: registrar(nombre, ip, puertoUsuario, contra, version)
* ARGS_IN: nombre: nombre del usuario que se desea registrar, ip del usuario que se va a registrar
            puertoUsuario a registrar, contra: contraseña del usuario y version: version más alta del usuario
* DESCRIPCIÓN: En esta funcion se lleva a cabo el registro en el servidor del usuario para que pueda ser localizado por el resto
                de usuarios
* ARGS_OUT: devuelve si el registro se ha producido o no de forma correcta
'''
def registrar(nombre, ip, puertoUsuario, contra, version):
    RegSocket = CrearSocket.crearSocket() # llamamos a crear socket que nos crea una conexión con el servidor
    mensaje = 'REGISTER ' + nombre + ' ' + ip +  ' ' + puertoUsuario + ' ' + contra + ' ' + 'V0'
    RegSocket.send(mensaje.encode()) # enviamos el mensaje para registrarnos y esperamos respuesta del servidor
    res = RegSocket.recv(1440)
    mensajeRes = res.decode()
    if mensajeRes[0:2] == 'OK': # si la respuesta contiene Ok es que el registro se ha realizado correctamente
        RegSocket.close()
        return 'Registro Correcto'
    else:
        RegSocket.close()
        return 'Registro Incorrecto'

'''
* FUNCIÓN: query(nombre)
* ARGS_IN: nombre: nombre del usuario que se desea obtener la información
* DESCRIPCIÓN: En esta funcion se llama al servidor para conocer la información necesaria para poder iniciar una llamada con
                otro usuario
* ARGS_OUT: en el caso de que el usuario exista un cadena con toda la información pertinente
'''
def query(nombre):
    RegSocket = CrearSocket.crearSocket() # abrimos el socket para contactar con el servidor
    mensaje = 'QUERY ' + nombre
    RegSocket.send(mensaje.encode()) # enviamos el mensaje de Query y esperamos una respuesta
    res = RegSocket.recv(1440)
    mensajeRes = res.decode().split(" ")
    # si devuelve ok devolvemos toda la información de dicho usuario
    if mensajeRes[0] == 'OK': 
        respuesta = mensajeRes[2] + ' ' + mensajeRes[3] + ' ' + mensajeRes[4] + ' ' + mensajeRes[5]
        RegSocket.close()
        return respuesta
    else:
        RegSocket.close()
        return 'Usuario no encontrado'

'''
* FUNCIÓN: query(nombre)
* ARGS_IN: ninguno
* DESCRIPCIÓN: En esta funcion se llama al servidor para conocer de todos los usuarios del servidor
* ARGS_OUT: listado con toda la información de cada uno de los usuarios
'''

def listUsers():
    RegSocket = CrearSocket.crearSocket() # abrimos el socket para contactar con el servidor
    mensaje = 'LIST_USERS'
    RegSocket.send(mensaje.encode()) # enviamos el mensaje de LIST_USERS y esperamos una respuesta
    tam = 1440
    respuesta = b''
    while tam == 1440:
        res = RegSocket.recv(1440)
        tam = len(res)
        respuesta += res # Vamos concatenando las respuestas mientras se reciban mensajes del tamaño estipulado
    mensajeRes = ' '.join(respuesta.decode().split(' ')[3:]) # separamos los usuarios del resto del mensaje
    mensaje = mensajeRes.split("#")
    listUsers = []
    # dividimos la información del mensaje de cada uno de los usuarios y obtenemos la información que deseamos
    for i in mensaje: 
        user = i.split(" ")
        if len(user) == 4:
            userInfo = user[0] + " " + user[1] + " " + user[2]
            listUsers.append(userInfo)
    RegSocket.close()
    return listUsers
'''
* FUNCIÓN: quit()
* ARGS_IN: ninguno
* DESCRIPCIÓN: En esta funcion se llama al servidor para decirle que cerramos la conexión
* ARGS_OUT: ninguno
'''
def quit():
    RegSocket = CrearSocket.crearSocket() # abrimos el socket para contactar con el servidor
    mensaje = 'QUIT' 
    RegSocket.send(mensaje.encode()) # enviamos el mensaje QUIT y salimos
    RegSocket.close()
    return

