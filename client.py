import socket
import time

def send_integer(host='localhost', port=12345, number=0):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                print("Connected to server.")
                client_socket.sendall(str(number).encode())
                response = client_socket.recv(1024)
                print(f'Received from server: {response.decode()}')
                break  # Exit the loop after successful communication
        except ConnectionRefusedError:
            print("Server is not available. Retrying in 2 seconds...")
            time.sleep(2)  # Wait before trying again

if __name__ == '__main__':
    # Example usage: sending the integer 10
    send_integer(number=10)
