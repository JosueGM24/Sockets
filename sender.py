import socket

def main():
    multicast_group = '224.1.1.1'  # Dirección del grupo multicast
    port_5004 = 5004                # Puerto para el primer receptor
    port_5000 = 5000                # Puerto para el segundo receptor
    
    # Crear el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        # Pedir la operación por teclado
        operacion = input("Ingrese una operación aritmética (o 'salir' para terminar): ")
        if operacion.lower() == 'salir':
            break
        
        # Enviar la operación al primer receptor
        sock.sendto(operacion.encode(), (multicast_group, port_5004))
        
        # Enviar la operación al segundo receptor
        sock.sendto(operacion.encode(), (multicast_group, port_5000))
        
        # Recibir la respuesta del servidor (si hay alguna lógica de recepción)
        # No implementado porque solo estamos enviando

    sock.close()

if _name_ == "_main_":
    main()