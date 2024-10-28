import socket
import struct

def handle_client(port, client_id):
    # Create a socket for each client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reuse of the port
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    host = '0.0.0.0'
    client_socket.bind((host, port))
    
    # Listen for the client
    client_socket.listen(1)
    print(f"Waiting for Client {client_id} on port {port}...")
    
    conn, addr = client_socket.accept()
    print(f"Client {client_id} connected from {addr} on port {port}")

    # Receive the message from the client
    message = conn.recv(1024).decode('utf-8')
    print(f"Client {client_id} sent: {message}")

    # Return the length of the message and the message itself
    conn.close()
    return len(message), message

def receive_integer_from_client(host, port, client_id):
    """Receives an integer from a client on a specified port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow reuse of the port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.bind((host, port))
        server_socket.listen(2)
        print(f"Waiting for Client {client_id} on port {port}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Client {client_id} connected from {addr}")
            data = conn.recv(1024)
            if not data:
                print(f"Client {client_id} did not send any data.")
                return None
            received_number = struct.unpack('d', data)[0]
            print(f"Client {client_id} sent: {received_number}")
            return received_number

def send_integer_to_client(host, port, client_id, number):
    """Sends an integer to a client on a specified port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow reuse of the port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.connect((host, port))
        print(f"Sending {number} to Client {client_id} on port {port}")
        data = struct.pack('d', number)  # Pack the number as a double
        server_socket.sendall(data)
        print(f"Sent {number} to Client {client_id}")

def start_server():
    # Define different ports for different clients
    ports = [12345, 12346]
    
    # Handle both clients on different ports
    lengths = []
    messages = []

    for i, port in enumerate(ports):
        length, message = handle_client(port, i + 1)
        lengths.append(length)
        messages.append(message)

    # Compare and print the message with the larger length
    if lengths[0] > lengths[1]:
        print(f"Client 1 has the longer message: {messages[0]} (Length: {lengths[0]})")
    elif lengths[1] > lengths[0]:
        print(f"Client 2 has the longer message: {messages[1]} (Length: {lengths[1]})")
    else:
        print(f"Both clients sent messages of the same length: {lengths[0]}")

if __name__ == '__main__':
    start_server()
    p1, p2 = 7696, 9467
    host = '0.0.0.0'

    # Receive integers from clients
    n1 = receive_integer_from_client(host, p1, 1)
    n2 = receive_integer_from_client(host, p2, 2)

    # Calculate the difference
    difference = abs(n1 - n2)
    
    # Determine which client has the larger value
    if n1 > n2:
        # Send the difference to Client 1 and 0 to Client 2
        send_integer_to_client('192.168.29.110', 7694, 1, difference)
        send_integer_to_client('192.168.29.79', 5005, 2, 0)
        print(f"Sent the difference {difference} to Client 1 and 0 to Client 2.")
    elif n2 > n1:
        # Send the difference to Client 2 and 0 to Client 1
        send_integer_to_client('192.168.29.79', 5005, 2, difference)
        send_integer_to_client('192.168.29.110', 7694, 1, 0)
        print(f"Sent the difference {difference} to Client 2 and 0 to Client 1.")
    else:
        # If both clients sent the same value, send 0 to both
        send_integer_to_client('192.168.29.110', 7694, 1, 0)
        send_integer_to_client('192.168.29.79', 5005, 2, 0)
        print(f"Both clients sent the same value, sent 0 to both clients.")
