import socket
import struct
from flask import Flask, request, redirect, url_for, render_template
import os
import json

app = Flask(__name__)

MULTICAST_GRP_1 = '224.1.1.1'
MULTICAST_GRP_2 = '224.1.1.2'
MULTICAST_PORT = 5004
CHUNK_SIZE = 1048576  # Ajuste a un tamaño seguro

def send_file(file_path, group):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    total_chunks = file_size // CHUNK_SIZE + (1 if file_size % CHUNK_SIZE > 0 else 0)

    with open(file_path, 'rb') as f:
        for chunk_index in range(total_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            message = {
                'filename': filename,
                'chunk_index': chunk_index,
                'total_chunks': total_chunks,
                'data': chunk_data.decode('latin-1')
            }
            sock.sendto(json.dumps(message).encode('latin-1'), (group, MULTICAST_PORT))

@app.route('/')
def index():
    files_group_1 = get_files_from_group(MULTICAST_GRP_1)
    files_group_2 = get_files_from_group(MULTICAST_GRP_2)
    return render_template('index.html', files_group_1=files_group_1, files_group_2=files_group_2)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    group = request.form.get('group')
    if file.filename == '' or group not in [MULTICAST_GRP_1, MULTICAST_GRP_2]:
        return redirect(request.url)
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        send_file(file_path, group)
        os.remove(file_path)  # Remove the file after sending
        return redirect(url_for('index'))

@app.route('/delete/<group>/<filename>')
def delete_file(group, filename):
    delete_file_from_group(group, filename)
    return redirect(url_for('index'))

def get_files_from_group(group):
    files = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.settimeout(0.5)
    try:
        while True:
            data, _ = sock.recvfrom(65536)  # Aumentar el tamaño del búfer de recepción
            message = json.loads(data.decode('latin-1'))
            if 'list' in message:
                files = message['list']
                break
    except socket.timeout:
        pass
    return files

def delete_file_from_group(group, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    message = {'delete': filename}
    sock.sendto(json.dumps(message).encode('latin-1'), (group, MULTICAST_PORT))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
