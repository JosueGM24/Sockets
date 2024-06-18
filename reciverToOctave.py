# receiver.py
import socket
import struct

def reciver_in_hex(mcast_grp, mcast_port, output_file):
    # Crear el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincular el socket al puerto
    sock.bind(('', mcast_port))

    # Unirse al grupo multicast
    mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Unido al grupo multicast {mcast_grp} en el puerto {mcast_port}")

    while True:
        print("Esperando datos...")
        data, address = sock.recvfrom(10240)
        print("Datos recibidos")
        operacion = data.decode('utf-8')
        print(f"Operación recibida: {operacion}")
        
        # Escribir la operación en el archivo
        with open(output_file, 'w') as f:
            f.write(operacion)

if __name__ == "__main__":
    reciver_in_hex('224.1.1.1', 5004, 'operacion.txt')
