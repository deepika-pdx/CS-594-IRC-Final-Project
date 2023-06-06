# This is a Simple IRC(Internet Replay Chat)Program. The program composed of IRC-server 
# connection anc IRC-client parts.  The basic commands for server are NICK, CREATE, JOIN, 
# LIST AND QUIT command.
# NICK – Give the user a nickname or change the previous one. The server should
#        report an error message if a user attempts to use an already-taken nickname.
# CREATE – Create a channel name.
# JOIN - Specify which channel do you want to join.
# LIST - List the available channels we have.
# PRIVMSG - PRIVMSG can send message to a specific room or client.
# QUIT – End the client session. The server should announce the client’s departure to
#        all other users sharing the channel with the departing client

# This program did not hand multiple clients join room but client can
# join multiple room.


    
import socket
import threading

# server address
server = 'localhost'
# port number 
port = 6667  
# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server, port))
#server can store 5 clients socket for each room
server_socket.listen(5) 
print('Connecting server...')

#Dictionary to store the rooms and their clients
rooms = {}

#Function to process all commands
def handle_command(command, client_socket, client_address):
    global rooms  #global veriables

    #command NICK
    if command.startswith('NICK'):
        parts = command.split()
        if len(parts) >= 2:
            nickname = parts[1]
            try:
                client_socket.send(bytes('Hello, {}!\r\n'.format(nickname), 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalide command. Usage: NICK <nickname>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    #command CREATE
    elif command.startswith('CREATE'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            if channel not in rooms:
                rooms[channel] = []
            rooms[channel].append(client_socket)
            try:
                client_socket.send(bytes('Create a channel: {}\r\n'.format(channel), 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: CREATE <channel>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

    #command JOIN
    elif command.startswith('JOIN'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            if channel not in rooms:
                rooms[channel] = []
            rooms[channel].append(client_socket)
            try:
                client_socket.send(bytes('Joined channel: {}\r\n'.format(channel), 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: JOIN <channel>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()

     #command Private message           
    elif command.startswith('PRIVMSG'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            if channel not in rooms:
                rooms[channel] = []
            rooms[channel].append(client_socket)
            try:
                client_socket.send(bytes('Private message@: {}\r\n'.format(channel), 'UTF-8'))
            except ConnectionResetError:
                    remove_client_from_rooms(client_socket)
                    client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: PRIVMSG<channel>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()   
    
    #command LIST
    elif command.startswith('LIST'):
        available_rooms = 'Available Channels:  {}'.format(' , '.join(rooms.keys()))
        try:
            client_socket.send(bytes(available_rooms + '\r\n', 'UTF-8'))
        except ConnectionResetError:
            remove_client_from_rooms(client_socket)
            client_socket.close()
    
    #command QUIT
    elif command.startswith('QUIT'):
        parts = command.split()
        if len(parts) >= 2:
            channel = parts[1]
            if channel in rooms:
                if client_socket in rooms[channel]:
                    rooms[channel].remove(client_socket)
                    try:
                        client_socket.send(bytes('Left channel, bye!: {}\r\n'.format(channel), 'UTF-8'))
                    except ConnectionResetError:
                        remove_client_from_rooms(client_socket)
                        client_socket.close()
            else:
                try:
                    client_socket.send(bytes('You are not in channel: {}\r\n'.format(channel), 'UTF-8'))
                except ConnectionResetError:
                    remove_client_from_rooms(client_socket)
                    client_socket.close()
        else:
            try:
                client_socket.send(bytes('Invalid command. Usage: LEAVE <channel>\r\n', 'UTF-8'))
            except ConnectionResetError:
                remove_client_from_rooms(client_socket)
                client_socket.close()


#Functions for error handling
def remove_client_from_rooms(client_socket):
    global rooms
    for channel in rooms.values():
        if client_socket in channel:
            channel.remove(client_socket)

#Functions for broadcast message
#This function is not working
def broadcast_message(room, message):
    if room in rooms:
        for client in rooms[room]:
            client.send(bytes(f':localhost {message}\r\n', 'UTF-8'))

# Accept client connections
client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

# Welcome message to the client
client_socket.send(b'Localhost 127.0.0.1 Welcome to the IRC_Server!\r\n')

# Continuously receive and process client messages
while True:
    try:
        message = client_socket.recv(2048).decode('UTF-8')
        print('Received:', message.strip())

        #handle client commands
        handle_command(message, client_socket, client_address)
    except ConnectionResetError:
        remove_client_from_rooms(client_socket)
        client_socket.close()
        break

# Close the server socket
server_socket.close()