import socket
import struct
import inflect

def numero_a_palabras(numero):
    p = inflect.engine()
    
    # Convertir la parte entera y la parte fraccionaria por separado
    partes = str(numero).split('.')
    parte_entera = int(partes[0])
    palabras_parte_entera = p.number_to_words(parte_entera)
    
    if len(partes) == 1:
        # Si no hay parte fraccionaria
        return palabras_parte_entera
    else:
        # Hay parte fraccionaria
        parte_fraccionaria = partes[1]
        palabras_parte_fraccionaria = ' '.join(p.number_to_words(int(digit)) for digit in parte_fraccionaria)
        return f"{palabras_parte_entera} point {palabras_parte_fraccionaria}"

def evaluar_operacion(operacion):
    try:
        resultado = eval(operacion)
        return resultado
    except Exception as e:
        return str(e)

def decimal_a_hexadecimal_con_fraccion(numero_decimal):
    if not isinstance(numero_decimal, (int, float)):
        return "El parámetro debe ser un número decimal."

    # Convertir la parte entera a hexadecimal
    parte_entera = int(numero_decimal)
    parte_entera_hex = hex(parte_entera).lstrip("0x") or "0"

    # Si el número es entero, retornar el resultado directamente
    if isinstance(numero_decimal, int):
        return parte_entera_hex

    # Convertir la parte fraccionaria a hexadecimal
    parte_fraccionaria = numero_decimal - parte_entera
    parte_fraccionaria_hex = []
    while parte_fraccionaria > 0:
        parte_fraccionaria *= 16
        digito_hex = int(parte_fraccionaria)
        parte_fraccionaria_hex.append(hex(digito_hex).lstrip("0x"))
        parte_fraccionaria -= digito_hex

        # Limitar a 10 dígitos para evitar bucles infinitos
        if len(parte_fraccionaria_hex) > 10:
            break

    parte_fraccionaria_hex = ''.join(parte_fraccionaria_hex) or "0"
    
    # Combinar las partes
    resultado_hex = f"{parte_entera_hex}.{parte_fraccionaria_hex}"
    return resultado_hex

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enlazar a INADDR_ANY para recibir paquetes en todas las interfaces
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Unido al grupo multicast {MCAST_GRP} en el puerto {MCAST_PORT}")

while True:
    print("Esperando datos...")
    data, _ = sock.recvfrom(10240)
    print("Datos recibidos")
    operacion = data.decode()  # Decodificar la operación recibida
    print(f"Operación recibida: {operacion}")
    print("Resultado en palabras:", numero_a_palabras(evaluar_operacion(operacion)))
