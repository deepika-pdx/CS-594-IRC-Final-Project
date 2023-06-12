import socket
import threading

# Dictionary to store the rooms and their clients
rooms_and_client_sockets = {}
rooms_and_users = {}
client_sockets_and_usernames = {}
# server address
server = '0.0.0.0'
# port number
port = 6667

instructions = '\nMENU:\n' \
               '1.CREATE ROOM (Usage: create <room number>)\n' \
               '2.DISPLAY ROOMS (Usage: display_rooms)\n' \
               '3.JOIN ROOM (Usage: join <room number>)\n' \
               '4.DISPLAY MEMBERS OF THE ROOM (Usage: display_members <room number>)\n' \
               '5.SEND MESSAGE TO ROOM (Usage: send <room number> "<message>")\n' \
               '6.LEAVE ROOM (Usage: leave <room number>)\n' \
               '7.DISPLAY ALL MEMBERS OF THE APP (Usage: display_all_members)\n' \
               '8.PRIVATE MESSAGE (Usage: private <username> "<messsage>")\n' \
               '9.SEND FILE TO A ROOM (Usage: send file <room number> <file path>)\n' \
               '10.QUIT (Usage: quit)\n' \
               '\nEnter the command of your choice:'


# Function to process all commands
def handle_client_commands(command, client_socket, client_address):
    global rooms_and_client_sockets  # global variables
    file_number = 0
    # command Username
    if command.startswith('Username'):
        parts = command.split()  # this has nick as value 0 and satvika as value 1
        if len(parts) >= 2:
            username = parts[1]
            if client_socket not in client_sockets_and_usernames:
                client_sockets_and_usernames[client_socket] = []
            client_sockets_and_usernames[client_socket].append(username)  # clients username list
            try:
                print("User " + username + " created ")
                client_socket.send(bytes('Hello, {}!\r\n'.format(username), 'UTF-8'))
                client_socket.send(b'Welcome to the IRC_Server!\r\n')  # Welcome message to the client
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: Username <username>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command CREATE
    elif command.startswith('create'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            try:
                if channel not in rooms_and_client_sockets:
                    rooms_and_client_sockets[channel] = []
                    client_socket.send(bytes('Created a room: {}\r\n'.format(channel), 'UTF-8'))
                else:
                    client_socket.send(bytes('Room: {} already exists!\r\n'.format(channel), 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: create <room number>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command Display users
    elif command.startswith('display_rooms'):
        available_rooms = 'Available rooms:  {}'.format(' , '.join(rooms_and_client_sockets.keys()))
        try:
            client_socket.send(bytes(available_rooms + '\r\n', 'UTF-8'))
        except ConnectionResetError:
            remove_client_from_rooms(client_socket)
            client_socket.close()

    # command JOIN
    elif command.startswith('join'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            if channel not in rooms_and_client_sockets:
                client_socket.send(bytes('Specified Room: {} does not exist!\r\n'.format(channel), 'UTF-8'))
            elif client_socket in rooms_and_client_sockets[channel]:
                client_socket.send(bytes("User " + str(client_sockets_and_usernames[client_socket][0]) + ' already present in the room: {}.\r\n'.format(channel), 'UTF-8'))
            else:
                rooms_and_client_sockets[channel].append(client_socket)
                if channel not in rooms_and_users:
                    rooms_and_users[channel] = []
                rooms_and_users[channel].append(client_sockets_and_usernames[client_socket][0])
                try:
                    client_socket.send(bytes('Joined room: {}\r\n'.format(channel), 'UTF-8'))
                except ConnectionResetError:
                    remove_client_from_rooms(client_socket)
                    client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: join <room number>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command display members of a room
    elif command.startswith('display_members'):
        try:
            parts = command.split()
            if len(parts) >= 2:
                channel = parts[1]
                if channel not in rooms_and_users or len(rooms_and_users[channel]) == 0:
                    client_socket.send(bytes('There are no members in room: ' + str(channel) + '\r\n', 'UTF-8'))
                else:
                    available_users = 'Available members:  {}'.format(' , '.join(rooms_and_users[channel]))
                client_socket.send(bytes(available_users + '\r\n', 'UTF-8'))
        except ConnectionResetError:
            remove_client_from_rooms(client_socket)
            client_socket.close()

    # command "leave <room number>"
    elif command.startswith('leave'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            try:
                if channel not in rooms_and_client_sockets:
                    client_socket.send(bytes('Specified room {} does not exist.\r\n'.format(channel), 'UTF-8'))
                elif channel not in rooms_and_users or client_sockets_and_usernames[client_socket][0] not in rooms_and_users[channel]:
                    client_socket.send(bytes('You are currently not present in the room {}.\r\n'.format(channel), 'UTF-8'))
                else:
                    clients_in_the_room = rooms_and_users[channel]
                    clients_in_the_room.remove(client_sockets_and_usernames[client_socket][0])
                    rooms_and_users[channel] = clients_in_the_room
                    client_socket.send(bytes('You left the room {}.\r\n'.format(channel), 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: leave <room number>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command Display users
    elif command.startswith('display_all_members'):
        all_members_list = []
        for each_client_socket in client_sockets_and_usernames:
            all_members_list.append(client_sockets_and_usernames[each_client_socket][0])
        all_available_members = 'All the available members are:  {}'.format(' , '.join(all_members_list))
        try:
            client_socket.send(bytes(all_available_members + '\r\n', 'UTF-8'))
        except ConnectionResetError:
            remove_client_from_rooms(client_socket)
            client_socket.close()

    # command "private <username> "<message>"
    elif command.startswith('private'):
        parts = command.split()
        if len(parts) > 2:
            private_user = parts[1]
            private_message = ' '.join(parts[2:])
            try:
                private_user_client_socket = None
                for each_client_socket in client_sockets_and_usernames:
                    if private_user in client_sockets_and_usernames[each_client_socket]:
                        private_user_client_socket = each_client_socket
                if private_user_client_socket is None:
                    client_socket.send(bytes('Specified user: {} does not exist.\r\n'.format(private_user), 'UTF-8'))
                private_user_client_socket.send(bytes("\n" + str(client_sockets_and_usernames[client_socket][0]) + ":>" + private_message + '\r\n', 'UTF-8'))
                client_socket.send(bytes('Message sent to the user {}.\r\n'.format(private_user), 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: private <username> <message>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command "send file <room number> <file content>
    elif command.startswith('send file'):
        parts = command.split()
        if len(parts) > 3:
            channel = parts[2]
            file_data = ' '.join(parts[3:])
            try:
                # Creating a new file at server end and writing the data
                received_file = str(client_sockets_and_usernames[client_socket][0]) + 'output' + str(file_number) + '.txt'
                file_number += file_number
                open_received_file = open(received_file, "w")
                if file_data:
                    open_received_file.write(file_data)
                # File is closed after data is sent
                open_received_file.close()
                client_socket.send(bytes('Received file from {}.\r\n'.format(client_sockets_and_usernames[client_socket][0]), 'UTF-8'))
                if channel not in rooms_and_client_sockets:
                    client_socket.send(bytes('Specified room {} does not exist.\r\n'.format(channel), 'UTF-8'))
                else:
                    # Reading file and sending to all the users in the given room
                    file_to_be_sent = open(received_file, "r")
                    send_file_data = file_to_be_sent.read()

                    clients_in_the_room = rooms_and_client_sockets[channel]
                    clients_to_which_file_is_sent = []
                    for each_client in clients_in_the_room:
                        if each_client != client_socket and each_client not in clients_to_which_file_is_sent:
                            if send_file_data:
                                each_client.send(bytes("send file" + ' ' + client_sockets_and_usernames[client_socket][0] + ' ' + str(send_file_data) + '\r\n', 'UTF-8'))
                            clients_to_which_file_is_sent.append(each_client)
                    # File is closed after data is sent
                    file_to_be_sent.close()
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: private <username> <message>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command send message to a room
    elif command.startswith('send'):
        parts = command.split()
        if len(parts) > 2:
            channel = parts[1]
            message = ' '.join(parts[2:])
            try:
                if channel not in rooms_and_client_sockets:
                    client_socket.send(bytes('Specified room {} does not exist.\r\n'.format(channel), 'UTF-8'))
                else:
                    # Send message to all the users in the given room
                    clients_in_the_room = rooms_and_client_sockets[channel]
                    clients_to_which_msg_is_sent = []
                    for each_client in clients_in_the_room:
                        if each_client != client_socket and each_client not in clients_to_which_msg_is_sent:
                            each_client.send(bytes(message + '\r\n', 'UTF-8'))
                            clients_to_which_msg_is_sent.append(each_client)
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: send <room number> <message>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    # command QUIT
    elif command.startswith('quit'):
        print(f"Client: {client_address} disconnected")
        for users in rooms_and_users.values():
            if client_sockets_and_usernames[client_socket][0] in users:
                users.remove(client_sockets_and_usernames[client_socket][0])
        client_sockets_and_usernames.pop(client_socket)
        remove_client_from_rooms(client_socket)
    else:
        client_socket.send(bytes('Invalid command: Type the command from the below list\r\n' + instructions, 'UTF-8'))


# Functions for error handling
def remove_client_from_rooms(client_socket):
    global rooms_and_client_sockets
    for channel in rooms_and_client_sockets.values():
        if client_socket in channel:
            channel.remove(client_socket)


# Functions for broadcast message
# This function is not working
def broadcast_message(room, message):
    if room in rooms_and_client_sockets:
        for client in rooms_and_client_sockets[room]:
            client.send(bytes(f":localhost {message}\r\n', 'UTF-8"))


# Continuously receive and process client messages
def process_client_messages(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(2048).decode('UTF-8')
            if not len(message):
                print("No msg received")
                remove_client_from_rooms(client_socket)
                client_socket.close()
            else:
                if "file" not in message:
                    print('Received:', message.strip())
                # handle client commands
                handle_client_commands(message, client_socket, client_address)
        except ConnectionResetError:
            remove_client_from_rooms(client_socket)
            client_socket.close()
            break


# Accept client connections
def accept_clients_messages():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Client {client_address} connected:')
        # Start separate thread to communicate with each client
        thread = threading.Thread(target=process_client_messages, args=(client_socket, client_address))
        thread.start()


# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server, port))
# server can store 5 clients socket for each room
server_socket.listen(5)
print('Server is in listening on ' + str(server) + ":" + str(port))

accept_clients_messages()

# Close the server socket
server_socket.close()