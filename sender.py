import socket

def main():
    multicast_group_1 = '224.1.1.1'  # Grupo multicast para las IPs 10.x.x.x
    multicast_group_2 = '224.1.1.2'  # Grupo multicast para las IPs 11.x.x.x
    
    port_5004 = 5004  # Puerto para el primer receptor
    port_5000 = 5000  # Puerto para el segundo receptor
    
    # Crear el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        # Pedir la operación por teclado
        operacion = input("Ingrese una operación aritmética (o 'salir' para terminar): ")
        if operacion.lower() == 'salir':
            break
        
        # Enviar la operación al primer grupo multicast (IPs 10.x.x.x)
        sock.sendto(operacion.encode(), (multicast_group_1, port_5004))
        sock.sendto(operacion.encode(), (multicast_group_1, port_5004))
        
        # Enviar la operación al segundo grupo multicast (IPs 11.x.x.x)
        sock.sendto(operacion.encode(), (multicast_group_2, port_5000))
        sock.sendto(operacion.encode(), (multicast_group_2, port_5000))
        
        # Recibir la respuesta del servidor (si hay alguna lógica de recepción)
        # No implementado porque solo estamos enviando

    sock.close()

if __name__ == "__main__":
    main()
