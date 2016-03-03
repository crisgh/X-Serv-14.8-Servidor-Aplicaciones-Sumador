#! /usr/bin/python
# -*-  coding: utf-8 -*-

#María Cristina Gallego Herrero
import socket

class webApp:

	def parse(self, request):
		return None

	def process(self, parsedRequest):
		return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

	def __init__(self, hostname, port):

		# Create a TCP objet socket and bind it to a port
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		mySocket.bind((hostname, port))

		# Queue a maximum of 5 TCP connection requests
		mySocket.listen(5)

		# Accept connections, read incoming data, and call
		# parse and process methods (in a loop)

		while True:
			print ('Waiting for connections')
			(recvSocket, address) = mySocket.accept()
			print ('HTTP request received (going to parse and process):')
			request = recvSocket.recv(2048)
			print (request)
			parsedRequest = self.parse(request)
			(returnCode, htmlAnswer) = self.process(parsedRequest)
			print ('Answering back...')
			recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
					+ htmlAnswer + "\r\n",'utf-8'))
			recvSocket.close()

class sumadorApp(webApp):
	def parse(self, request):
		try :
			numero = int(request.split()[1][1:])
			valido = True
		except ValueError:
			valido = False
			numero = 0
		return numero,valido #lista de valores
	def process(self, parsedRequest):
		numero,valido = parsedRequest
		if not valido:
			return ("200 OK", "<html><body><h1> Solo uso valores enteros </h1></body></html>")
		if self.esPrimero :
			self.primer_numero = numero #lo hacemos variable global --> Atributo
			self.esPrimero = False
			return ("200 OK", "<html><body><h1> Introduce el siguiente numero de la suma </h1></body></html>")
		else:
			segundo_numero = numero
			suma = self.primer_numero + segundo_numero
			self.esPrimero = True
			return("HTTP/1.1 200 OK\r\n\r\n" ,
					"<html><body><h1>" + " La suma es : " + str(suma)
					+ "</h1></body></html>" + "\r\n")
	def __init__(self,hostname,port):
		self.esPrimero = True
		super(sumadorApp,self).__init__(hostname,port)

try:
	if __name__ == "__main__":
		sumador = sumadorApp("localhost", 2312)
except KeyboardInterrupt:
    print ("Servidor cerrado")
    mySocket.close()
