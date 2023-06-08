# This file is IRC_client script, which can process commands from IRC_server part.

import socket
import threading
import sys

server = 'localhost'  # server address
port = 6667  # port number 

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server, port))
print('Connected to the server.')

name = input('Enter your nickname:')
client_socket.send(bytes(f'NICK {name}\r\n', 'UTF-8'))


room = input('Enter the room name: ')
client_socket.send(bytes(f'JOIN {room}\r\n', 'UTF-8'))

#Function to change Nick name
def send_message():
    while True:
        message = input()
        client_socket.send(bytes(message + '\r\n', 'UTF-8'))

#Function to send private message to a room
def send_messages():
    while True:
        message = input()
        if message.startswith('/'):
            command, *args = message.split()
            if command == '/send':
                if args:
                    target_room = args[0]
                    if len(args) > 1:
                        message = ' '.join(args[1:])
                        client_socket.send(bytes(f'PRIVMSG {target_room} :{message}\r\n', 'UTF-8'))
                    else:
                        print('Please provide a message to send.')
                else:
                    print('Please provide the room name as an argument.')
            else:
                print('Invalid command.')
        else:
            client_socket.send(bytes(f'PRIVMSG {room} :{message}\r\n', 'UTF-8'))

# Function to receive and process server messages
def receive_messages():
    while True:
        try:
            message = client_socket.recv(2048).decode('UTF-8')          
            if not message:
                break
            print('->:', message.strip())

            # Process server commands
        except ConnectionResetError:
            break
        except ConnectionResetError:
            break
        except OSError as e:
            if e.errno == 10053:
                break
            else:
                raise e

# Start a separate thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Function to send commands to the server
def send_command():
    while True:
        command = input('Enter command: (commands include: DISPLAYUSERS/CREATE/JOIN/PRIVMSG/LIST/QUIT)\r\n')
        if command.lower() == 'quit':
            break
        client_socket.send(bytes(command + '\r\n', 'UTF-8'))

# Start a separate thread to send commands to the server
send_thread = threading.Thread(target=send_command)
send_thread.start()

# Wait for the send thread to finish
send_thread.join()

# Close the client socket
client_socket.close()
