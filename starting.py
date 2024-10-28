import paramiko
import time

def run_interactive_script(hostname, port, username, password, script_path):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        ssh.connect(hostname, port=port, username=username, password=password)

        # Open a transport and invoke a shell
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.get_pty()  # Allocate a pseudo-terminal
        channel.invoke_shell()  # Start a shell session

        # Send the command to run the script
        channel.send(f'python3 {script_path}\n')

        # Wait for the command to complete
        time.sleep(2)

        # Print the output
        while channel.recv_ready():
            output = channel.recv(1024).decode('utf-8')
            print(output)

        # Clean up
        channel.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the SSH connection
        ssh.close()


# Example usage
if __name__ == "__main__":
    HOSTNAME = "192.168.29.110"  # IP address of the remote machine
    PORT = 22                   # SSH port
    USERNAME = "ktk"  # Your SSH username
    PASSWORD = "ktk123"  # Your SSH password
    SCRIPT_PATH = "/home/ktk/hello.py"  # Path to the script on the remote machine

    run_interactive_script(HOSTNAME, PORT, USERNAME, PASSWORD, SCRIPT_PATH)
