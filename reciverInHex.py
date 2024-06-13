import socket
import struct

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

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5004

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('10.0.0.2', MCAST_PORT))  # Cambia la IP a 10.0.0.2
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Unido al grupo multicast {MCAST_GRP} en el puerto {MCAST_PORT}")

while True:
    print("Esperando datos...")
    data, _ = sock.recvfrom(10240)
    print("Datos recibidos")
    operacion = data.decode()  # Decodificar la operación recibida
    print(f"Operación recibida: {operacion}")
    print("Resultado en hexadecimal:", decimal_a_hexadecimal_con_fraccion(evaluar_operacion(operacion)))
