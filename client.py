import socket
import sys
def main():
    try: 
        socket_cliente=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("No se pudo crear el socket")
        sys.exit()
    print("socket creado")
    target_host="127.0.0.1"
    target_port="9500"
    BUFSIZE=256
    payload="Hola servidor"
    socket_cliente.connect((target_host,int(target_port)))
    try:
        while true:
            print("socket conectado a %s", target_host)
            socket_cliente.send(payload.encode("UTF-8"))
            print("Mensaje del servidor")
            data=socket_cliente.recv(BUFSIZE)
            print(data)
    except keyboardInterrupt:
        print("Condicion terminada por el usuario")
        sys.exiit()
main()
