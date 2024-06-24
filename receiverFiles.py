import socket
import struct
import os

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5004
UPLOAD_FOLDER = 'received_files_group_1'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Unido al grupo multicast {MCAST_GRP} en el puerto {MCAST_PORT}")

while True:
    print("Esperando datos...")
    data, _ = sock.recvfrom(10240)
    print("Datos recibidos")
    filename = os.path.join(UPLOAD_FOLDER, 'received_file')  # Customize filename as needed
    save_file(data, filename)
    print(f"Archivo recibido y guardado como: {filename}")
