import socket

def evaluar_operacion(operacion):
    try:
        resultado = eval(operacion)
        return resultado
    except Exception as e:
        return str(e)


def decimal_a_hexadecimal(numero_decimal):
    try:
        hexadecimal = hex(numero_decimal)
        return hexadecimal
    except Exception as e:
        return str(e)


group = '224.1.1.1'
port = 5004

# 2-hop restriction in network
ttl = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Pide por teclado la operacion y envíalo por el socket sustituyendo el mensaje "hello world"
while True:
    operacion = input("Ingrese una operación aritmética (o 'salir' para terminar): ")
    if operacion.lower() == 'salir':
        break
    
    sock.sendto(operacion.encode(), (group, port))
    
sock.close()
