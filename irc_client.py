import socket
import sys
import threading

server_IP_address = "127.0.0.1"
server_port = 1234

input_name = input("Enter your name: ")

# Creating client socket and connecting to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_IP_address, server_port))
#client_socket.setblocking(False)

#Below code is to Receive and print the messages
def Receive_Fun():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'MSG_PROVIDE_NAME':
                client_socket.send(input_name.encode('utf-8'))
            elif message == 'MSG_QUIT':
                print("quit msg frm srv: ", message)
                client_socket.close()
                sys.exit(2)
            else:
                print(message)
        except Exception as e:
            print('Server not responding')
            client_socket.close()
            sys.exit(2)

#Function to send messages to the server
def Send_Fun():
    while True:
        input_msg = input('')
        try:
            if input_msg == '1' or input_msg =='DISPLAY ROOMS':
                message = input_name + " MSG_DISPLAY_ROOMS "
            elif input_msg == '2' or input_msg =='CREATE ROOM':
                roomname = input('Enter room name to create: ')
                message = input_name + " MSG_CREATE_ROOM " + roomname
            elif input_msg == '3' or input_msg =='JOIN ROOM':
                roomname = input("Enter room name to join: ")
                message = input_name + " MSG_JOIN_ROOM " + roomname
            elif input_msg == '4' or input_msg =='SWITCH ROOMS':
                roomname = input("Enter room name to switch: ")
                message = input_name + " MSG_SWITCH_ROOM " + roomname
            elif input_msg == '5' or input_msg =='DISPLAY USERS':
                message = input_name + " MSG_DISPLAY_USERS "
            elif input_msg == '6' or input_msg =='DIRECT MESSAGE':
                msg = input("Send direct message: ")
                message = input_name + " MSG_DIRECT_MESSAGE " + msg
            elif input_msg == '7' or input_msg =='LEAVE ROOM':
                roomname = input("Enter room name to leave: ")
                message = input_name + " MSG_LEAVE_ROOM " + roomname
            elif input_msg == '8' or input_msg =='DISPLAY MENU':
                message = input_name + " MSG_HELP "
            elif input_msg == '9' or input_msg =='QUIT':
                message = input_name + " MSG_QUIT "
            else:
                print(" new functionality yet to be added")

            #print("Message sent by client: ", message)
            client_socket.send(message.encode('utf-8'))
        except:
            sys.exit(0)

#Start the receive thread
Threads_list = []
receive_thread = threading.Thread(target=Receive_Fun)
receive_thread.start()
Threads_list.append(receive_thread)

#Start the send thread
send_thread = threading.Thread(target=Send_Fun)
send_thread.start()
Threads_list.append(send_thread)


