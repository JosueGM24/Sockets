import socket
import struct
import os
import inflect

# Función para recibir y guardar archivos
def recibir_archivo(sock):
    data, addr = sock.recvfrom(102400)  # Ajustar tamaño máximo del archivo recibido
    nombre_archivo = 'archivo_recibido.bin'  # Nombre de archivo temporal
    with open(nombre_archivo, 'wb') as f:
        f.write(data)
    return nombre_archivo

# Función para convertir número a palabras
def numero_a_palabras(numero):
    p = inflect.engine()
    partes = str(numero).split('.')
    parte_entera = int(partes[0])
    palabras_parte_entera = p.number_to_words(parte_entera)
    if len(partes) == 1:
        return palabras_parte_entera
    else:
        parte_fraccionaria = partes[1]
        palabras_parte_fraccionaria = ' '.join(p.number_to_words(int(digit)) for digit in parte_fraccionaria)
        return f"{palabras_parte_entera} point {palabras_parte_fraccionaria}"

# Función para evaluar operación matemática
def evaluar_operacion(operacion):
    try:
        resultado = eval(operacion)
        return resultado
    except Exception as e:
        return str(e)

# Función para convertir decimal a hexadecimal con fracción
def decimal_a_hexadecimal_con_fraccion(numero_decimal):
    if not isinstance(numero_decimal, (int, float)):
        return "El parámetro debe ser un número decimal."
    parte_entera = int(numero_decimal)
    parte_entera_hex = hex(parte_entera).lstrip("0x") or "0"
    if isinstance(numero_decimal, int):
        return parte_entera_hex

    parte_fraccionaria = numero_decimal - parte_entera
    parte_fraccionaria_hex = []
    while parte_fraccionaria > 0:
        parte_fraccionaria *= 16
        digito_hex = int(parte_fraccionaria)
        parte_fraccionaria_hex.append(hex(digito_hex).lstrip("0x"))
        parte_fraccionaria -= digito_hex
        if len(parte_fraccionaria_hex) > 10:
            break

    parte_fraccionaria_hex = ''.join(parte_fraccionaria_hex) or "0"
    resultado_hex = f"{parte_entera_hex}.{parte_fraccionaria_hex}"
    return resultado_hex

# Función para listar archivos almacenados
def listar_archivos():
    return [nombre_archivo for nombre_archivo in os.listdir() if os.path.isfile(nombre_archivo)]

# Función para eliminar archivo
def borrar_archivo(nombre_archivo):
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
        return True
    return False

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5004

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Unido al grupo multicast {MCAST_GRP} en el puerto {MCAST_PORT}")

while True:
    print("Esperando datos...")
    # Recibir archivo y guardar
    archivo_recibido = recibir_archivo(sock)
    print(f"Archivo recibido y guardado: {archivo_recibido}")

    # Procesar archivo (ejemplo: convertir a palabras)
    with open(archivo_recibido, 'rb') as f:
        contenido = f.read().decode('utf-8')  # Decodificar archivo recibido si es texto

    # Ejemplo de procesamiento adicional
    resultado_procesamiento = numero_a_palabras(evaluar_operacion(contenido))
    print("Resultado en palabras:", resultado_procesamiento)

    # Eliminar archivo temporal
    os.remove(archivo_recibido)

    # Enviar respuesta opcional al sender si es necesario
    #sock.sendto(resultado_procesamiento.encode(), addr)

# Cerrar socket al finalizar
sock.close()

