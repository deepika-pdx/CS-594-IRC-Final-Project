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

name = input('Enter your name:')
client_socket.send(bytes(f'Username {name}\r\n', 'UTF-8'))


# Function to receive and process server messages
def receive_messages():
    while True:
        try:
            message = client_socket.recv(2048).decode('UTF-8')
            if not message:
                print("Server closed the connection")
                sys.exit()
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

instructions = '\nMENU:\n' \
               '1.CREATE ROOM (Usage: create <room number>)\n' \
               '2.DISPLAY ROOMS (Usage: display_rooms)\n' \
               '3.JOIN ROOM (Usage: join <room number>)\n' \
               '4.DISPLAY MEMBERS OF THE ROOM (Usage: display_members <room number>)\n' \
               '5.SEND MESSAGE TO ROOM (Usage: send <room number> "<message>")\n' \
               '6.LEAVE ROOM (Usage: leave <room number>)\n' \
               '7.DISPLAY ALL MEMBERS OF THE APP (Usage: display_all_members)\n' \
               '8.PRIVATE MESSAGE (Usage: private <username> "<messsage>")\n' \
               '9.QUIT (Usage: quit)\n' \
               '\nEnter the command of your choice:'


# Function to send commands to the server
def send_command():
    menu_count = 1
    while True:
        if menu_count == 1:
            command = input(instructions)
            menu_count += 1
        else:
            command = input(":>")
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