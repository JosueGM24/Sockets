import socket
import sys
HOST='LOCALHOST'
PORT= 9500
BUFSIZE=1024
ADDR=(HOST,PORT)
def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5) #encola un maximo de 5
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    while (True):
        print("Esperando conexion...")
        cliente_sock,addr=server_socket.accept()
        print("Cliente conectado desde: ", addr)
        data=cliente_sock.recv(BUFSIZE)
        print("mensaje del cliente: %s",data)
        print("mandando saludos al cliente")
        cliente_sock.send("Saludo recibido")
    server_socket.close()
main()