def recv_all(socket=None) -> str:
    """Receive all data from socket using null-byte terminator."""
    message = b''
    done = False
    while not done:
        chunk = socket.recv(1024)
        if not chunk:
            done = True
        if b'\x00' in chunk:
            chunk = chunk[:-1]
            done = True
        message += chunk
    return message.decode('utf-8')


def send_all(socket=None, message: str=None) -> None:
    """Write data to socket with terminating null byte."""
    socket.sendall(message.encode('utf-8') + b'\x00')
