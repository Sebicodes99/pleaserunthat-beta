import socket

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

            if request == '1':
                # Process the request if it's 1
                process_request()

            # Close the client socket
            client_socket.close()

    if status == "client":
        # Declare value of what to send
        petition = input("What do you want to execute? ")
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = ('ServerIp', 1234)

        # Connect to the server
        client_socket.connect(server_address)

        # Send the request to the server
        client_socket.send(petition.encode())

        # Close the client socket
        client_socket.close()
