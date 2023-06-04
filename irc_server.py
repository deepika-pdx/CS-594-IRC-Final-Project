import socket
import select

# Assigning server IP address and Port number
server_ip_address = "127.0.0.1"
server_port = 1234

# Creating a server socket instance and binding it with the declared port number
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_ip_address, server_port))
server_socket.listen()

# Creating a list for storing the client sockets
client_socket_list = [server_socket]

# Storing client connection details
clients = {}
print(f"Listening for client connections on {server_ip_address}:{server_port}")


# Processing received client messages
def receive_client_message(client_conn):
    try:
        message_header = client_conn.recv(10)
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_conn.recv(message_length)}
    except:
        return False


# Accepting client connections and reading and storing client messages
while True:
    read_client_sockets, _, exception_client_sockets = select.select(client_socket_list, [], client_socket_list)
    for each_client_socket in read_client_sockets:
        # Handling new client connections
        if each_client_socket == server_socket:
            client_conn, client_address = server_socket.accept()
            client_data = receive_client_message(client_conn)

            if client_data is False:
                continue

            client_socket_list.append(client_conn)
            clients[client_conn] = client_data
            print(f"Accepted new client connection having address: {client_address[0]} and port: {client_address[1]}")
        # Handling messages from existing connected clients
        else:
            client_message = receive_client_message(each_client_socket)
            # Handling clients that closed the connection with server
            if client_message is False:
                print('Closed connection from: {}'.format(clients[each_client_socket]['data'].decode('utf-8')))
                client_socket_list.remove(each_client_socket)
                del clients[each_client_socket]
                continue
            # Handling and sharing the clients messages to other clients
            # Fetching client message
            client = clients[each_client_socket]
            print(f"Received message from client: {client['data'].decode('utf-8')}: {client_message['data'].decode('utf-8')}")

            # Sharing the client message to other clients connected to the server
            for client_conn in clients:
                if client_conn != each_client_socket:
                    client_conn.send(client['header'] + client['data'] + client_message['header'] + client_message['data'])

        for client_socket in exception_client_sockets:
            # Remove from list for client sockets
            client_socket_list.remove(client_socket)

            # Remove from our list of clients
            del clients[client_socket]

