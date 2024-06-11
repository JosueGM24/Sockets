import socket

def main():
    group = 'localhost'  # Dirección del servidor
    port = 12345         # Puerto en el que el servidor está escuchando
    
    # Crear el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        # Pedir la operación por teclado
        operacion = input("Ingrese una operación aritmética (o 'salir' para terminar): ")
        if operacion.lower() == 'salir':
            break
        
        # Enviar la operación al servidor
        sock.sendto(operacion.encode(), (group, port))
        
        # Recibir la respuesta del servidor
        data, server = sock.recvfrom(1024)
        print(f"Resultado: {data.decode()}")

    sock.close()

if __name__ == "__main__":
    main()
