import socket
import sys
def main():
    try:
        socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as err:
        print("no se pudo crear el socket")
        sys.exit()
        print("socket creado")
        target_host="12.0.0.1"
        target_port="9500"
        BUFSIZE=256
        payload='hola ll'
        socket_cliente.connect((target_host,int(target_port)))
    print("socket creado")
    
    try:
        target_host="12.0.0.1"
        target_port="9500"
        BUFSIZE=256
        payload='HOLAAAA'
        socket_cliente.connect((target_host,int(target_port)))
        while True:
            print("socket conectado a ",target_host)
            socket_cliente.sendall(payload.encode('utf-8'))
            print("mensaje del servidor")
            data=socket_cliente.recv(BUFSIZE)
            print(data)
    except KeyboardInterrupt:
        print("Conexion terminada por el usuario")
        sys.exit()
main()
