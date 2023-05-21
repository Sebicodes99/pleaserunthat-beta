import socket
import os

# Config
server_ip = "Enter your private ip for a server"
server_port = 1234

status = input("Do you want to act as a client or server? ")

while True:
    def process_request():
        # Function to run when a petition is received
        print("Processing request...")


    if status == "server":
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = (server_ip, server_port)

        # Bind the socket to the server address and port
        server_socket.bind(server_address)

        # Listen for incoming connections
        server_socket.listen(1)

        print('Server listening on {}:{}'.format(*server_address))

        while True:
            # Wait for a client to connect
            print('Waiting for a connection...')
            client_socket, client_address = server_socket.accept()
            print('Connection established with:', client_address)

            # Receive the request from the client
            request = client_socket.recv(1024).decode()

            try:
                # Execute the request as a Linux/Mac terminal command
                os.system(request)
            except Exception as e:
                print("Error executing request:", e)

            # Close the client socket
            client_socket.close()

    if status == "client":
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_ip = input("What server do you want to connect to? ")
        server_port = input("What port do you want to use? ")
        server_port = int(server_port)
        server_address = (server_ip, server_port)

        # Connect to the server
        client_socket.connect(server_address)

        print("1) Shutdown Server")
        print("2) Reboot Server")
        print("3) Custom")
        code = input("What do you want to run? ")
        if code == "1":
            client_socket.send("poweroff".encode())
        elif code == "2":
            client_socket.send("reboot".encode())
        elif code == "3":
            # Send the request to the server
            petition = input("What do you want to run? ")
            client_socket.send(petition.encode())

        # Close the client socket
        client_socket.close()
