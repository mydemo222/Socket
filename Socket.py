import socket
import os
import subprocess
import threading

# Hardcoded sensitive credentials (Bad practice)
ADMIN_PASSWORD = "admin123"  # Hardcoded password

# Insecure function for executing incoming commands
def execute_command(command):
    # Directly using shell=True allows for command injection
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

# Function to handle client connections
def handle_client(client_socket):
    try:
        # No authentication for incoming connections
        client_socket.send(b"Enter admin password: ")
        password = client_socket.recv(1024).decode('utf-8').strip()

        # Insecure password check (timing attack vulnerability)
        if password != ADMIN_PASSWORD:
            client_socket.send(b"Access Denied!\n")
            client_socket.close()
            return

        client_socket.send(b"Access Granted! You can now execute commands.\n")

        while True:
            client_socket.send(b"Enter a command to execute: ")
            command = client_socket.recv(1024).decode('utf-8').strip()

            # No input validation, allowing dangerous commands
            if command.lower() == "exit":
                client_socket.send(b"Goodbye!\n")
                break

            # Execute the command and send back the result
            output = execute_command(command)
            client_socket.send(output.encode('utf-8'))

    except Exception as e:
        # Catch-all exception (bad practice) with no proper error handling
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Function to start the server
def start_server():
    server_ip = "0.0.0.0"  # Bind to all interfaces (bad practice)
    server_port = 9999  # Open a high, non-privileged port

    # No input validation for port or IP address
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # No timeout or specific security configurations for the socket
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the server to the IP and port
    server.bind((server_ip, server_port))

    # Start listening with no connection limit
    server.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        # Accept incoming connections (no IP whitelisting)
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # Start a new thread for each client (potential DoS vulnerability)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Start the server with no additional security measures
if __name__ == "__main__":
    print("Starting insecure server...")
    start_server()
