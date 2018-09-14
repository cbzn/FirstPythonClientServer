import socket

ip = 'localhost' #0.0.0.0'
puerto = 9797 # Puerto donde escucha el servidor
dataConection = (ip, puerto)
conexionesMaximas = 5

# Creamos el servidor.
# socket.AF_INET para indicar que utilizaremos Ipv4
# socket.SOCK_STREAM para utilizar TCP/IP (no udp)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketServidor.bind(dataConection)       # Asignamos los valores del servidor
socketServidor.listen(conexionesMaximas) # Asignamos el número máximo de conex

print('Server: Esperando conexiones en %s: %s' %(ip, puerto))
print(socket.gethostname())


# Bucle de escucha. En él indicamos la forma de actuar al recibir las
# tramas del cliente
while True:
    cliente, direccion = socketServidor.accept()
    while True:
        print('DIR: ', direccion)
        print()

        datos = cliente.recv(1024) #número maximo de bytes
        if datos == b'exit' or datos == b'GLOBALEXIT':
            cliente.send('exit'.encode())
            cliente.close()
            break
        else:
            print('Server: RECIBIDO: %s' %datos.decode())
            cliente.sendall(('-- Recibido --').encode())
    #cliente.close()
    print("------- CONEXIÓN CERRADA ---------")
    print()
    if datos == b'GLOBALEXIT':
        break    

print()
print("Server: Cerrando Servidor")
#socketServidor.close()
