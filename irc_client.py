import socket
import sys
import errno

server_IP_address = "127.0.0.1"
server_port = 1234

input_name = input("Enter a name: ")

# Creating client socket and connecting to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_IP_address, server_port))
client_socket.setblocking(False)

# Sending client information to the server
client_name = input_name.encode('utf-8')
client_header = f"{len(client_name):<10}".encode('utf-8')
client_socket.send(client_header + client_name)

# Sending messages to the server
while True:
    client_message = input(f"{input_name}> ")
    if client_message:
        client_message = client_message.encode('utf-8')
        client_message_header = f"{len(client_message):<10}".encode('utf-8')
        client_socket.send(client_message_header + client_message)

    # Receive messages from the server
    try:
        while True:
            received_sender_header = client_socket.recv(10)
            if not len(received_sender_header):
                print("Server closed the connection")
                sys.exit()

            received_sender_length = int(received_sender_header.decode('utf-8').strip())
            sender_name = client_socket.recv(received_sender_length).decode('utf-8')

            received_msg_header = client_socket.recv(10)
            received_msg_length = int(received_msg_header.decode('utf-8').strip())
            received_msg = client_socket.recv(received_msg_length).decode('utf-8')

            print(f"{sender_name}> {received_msg}")
    except IOError as e:
        # In case of no incoming data, continue as normal
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error while reading messages: {}'.format(str(e)))
            sys.exit()
        continue
    except Exception as e:
        print("Error in receiving messages from the server: " + str(e))
        sys.exit()



