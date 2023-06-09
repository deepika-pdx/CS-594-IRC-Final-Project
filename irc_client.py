# This file is IRC_client script, which can process commands from IRC_server part.

import socket
import threading
import sys

#server = '35.212.252.20'  # server address
server = 'localhost'
port = 6667  # port number

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server, port))
print('Connected to the server.')

name = input('Enter your name:')
client_socket.send(bytes(f'Username {name}\r\n', 'UTF-8'))
file_number = 0


# Function to receive and process server messages
def receive_messages():
    global file_number
    while True:
        try:
            message = client_socket.recv(2048).decode('UTF-8')
            if not message:
                print("Server closed the connection")
                sys.exit()
            elif message.startswith('send file'):
                parts = message.split()
                if len(parts) > 2:
                    received_from = parts[2]
                    file_data = ' '.join(parts[3:])
                    try:
                        # Creating a new file at server end and writing the data
                        received_file = str(name) + 'output' + str(file_number) + '.txt'
                        file_number += file_number
                        open_received_file = open(received_file, "w")
                        if file_data:
                            open_received_file.write(file_data)
                        # File is closed after data is sent
                        open_received_file.close()
                        print(f"Received a file from {received_from}.")
                    except Exception as e:
                        print("Error while receiving file from server: " + str(e))
            else:
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
               '9.SEND FILE TO A ROOM (Usage: send file <room number> <file path>)\n' \
               '10.QUIT (Usage: quit)\n' \
               '\nEnter the command of your choice:'


# Function to send commands to the server
def send_command():
    menu_count = 1
    try:
        while True:
            if menu_count == 1:
                command = input(instructions)
                menu_count += 1
            else:
                command = input(":>")
            if command.lower() == 'quit':
                client_socket.send(bytes(command + '\r\n', 'UTF-8'))
                break
            elif command.startswith('send file'):
                parts = command.split()
                if len(parts) > 3:
                    channel = parts[2]
                    file_path = parts[3]
                    try:
                        # Reading file and sending data to server
                        file_to_be_sent = open(file_path, "r")
                        file_data = file_to_be_sent.read()
                        if file_data:
                            command_to_be_sent_to_server = ' '.join(parts[0:3])
                            client_socket.send(bytes(command_to_be_sent_to_server + ' ' + str(file_data) + '\r\n', 'UTF-8'))
                        # File is closed after data is sent
                        file_to_be_sent.close()
                    except Exception as e:
                        print("Error while sending file to the server" + str(e))
            else:
                client_socket.send(bytes(command + '\r\n', 'UTF-8'))
    except Exception as e:
        if "An existing connection was forcibly closed by the remote host" in str(e):
            print('\nServer connection closed')
        else:
            print('\nClient connection closed')
        sys.exit()


# Start a separate thread to send commands to the server
send_thread = threading.Thread(target=send_command)
send_thread.start()

# Wait for the send thread to finish
send_thread.join()

# Close the client socket
client_socket.close()