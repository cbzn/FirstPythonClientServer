import socket # Utilidades de red y conexion

# Declaramos las variables
ipServidor = "localhost" #"127.0.0.1" # Es lo mismo que "localhost" o "0.0.0.0"
puertoServidor = 9797

# Configuramos los datos para conectarnos con el servidor
# socket.AF_INET para indicar que utilizaremos Ipv4
# socket.SOCK_STREAM para utilizar TCP/IP (no udp)
# Estos protocolos deben ser los mismos que en el servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ipServidor, puertoServidor))
print("Cliente: Conectado con el servidor ---> %s:%s" %(ipServidor, puertoServidor))

while True:
    msg = input("> ")
    cliente.send(msg.encode())
    respuesta = cliente.recv(4096)
    print('Server responded: ', respuesta.decode())
    if respuesta == b"exit":
        break
cliente.close()

print("------- CONEXIÓN CERRADA ---------")
print("Cliente: Closing Client")


