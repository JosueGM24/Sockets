import socket
import struct
import os
import json

MCAST_GRP = '224.1.1.2'
MCAST_PORT = 5004
CHUNK_SIZE = 1048576  # Ajustar al mismo tamaño que en el sender
RECEIVED_FILES_DIR = 'received_files_group_2'

if not os.path.exists(RECEIVED_FILES_DIR):
    os.makedirs(RECEIVED_FILES_DIR)

def save_chunk(filename, chunk_index, data):
    filepath = os.path.join(RECEIVED_FILES_DIR, f"{filename}.part{chunk_index}")
    with open(filepath, 'wb') as f:
        f.write(data)

def assemble_file(filename, total_chunks):
    filepath = os.path.join(RECEIVED_FILES_DIR, filename)
    with open(filepath, 'wb') as output_file:
        for chunk_index in range(total_chunks):
            chunk_path = os.path.join(RECEIVED_FILES_DIR, f"{filename}.part{chunk_index}")
            with open(chunk_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
            os.remove(chunk_path)  # Eliminar archivo de chunk después del ensamblado

def get_files_list():
    return os.listdir(RECEIVED_FILES_DIR)

def delete_file(filename):
    filepath = os.path.join(RECEIVED_FILES_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

def multicast_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Unido al grupo multicast {MCAST_GRP} en el puerto {MCAST_PORT}")

    received_files = {}
    while True:
        print("Esperando datos...")
        data, _ = sock.recvfrom(65536)  # Aumentar el tamaño del búfer de recepción
        print("Datos recibidos")
        message = json.loads(data.decode('latin-1'))

        if 'filename' in message:
            filename = message['filename']
            chunk_index = message['chunk_index']
            total_chunks = message['total_chunks']
            chunk_data = message['data'].encode('latin-1')

            save_chunk(filename, chunk_index, chunk_data)

            if filename not in received_files:
                received_files[filename] = [0] * total_chunks
            received_files[filename][chunk_index] = 1

            if all(received_files[filename]):
                assemble_file(filename, total_chunks)
                print(f"Archivo {filename} ensamblado y guardado.")
                del received_files[filename]

        if 'list' in message:
            files_list = get_files_list()
            response_message = {'list': files_list}
            sock.sendto(json.dumps(response_message).encode('latin-1'), (MCAST_GRP, MCAST_PORT))

        if 'delete' in message:
            delete_file(message['delete'])
            print(f"Archivo {message['delete']} eliminado.")

if __name__ == "__main__":
    multicast_receiver()
