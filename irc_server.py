import socket
import select
import threading

#Global lists and dictionaries
Clients_list = []
Nick_names_list = []
Room_object_dict = {}      #this dictionary maps roomname to room_object
Clients_socket_dict = {}   #this dictionary maps nickname to client_socket
Users_object_dict = {}     #this dictionary maps nickname to user_object

# Assigning server IP address and Port number
server_ip_address = "127.0.0.1"
server_port = 1234

instructions = '\nMENU:\n' \
               '1.DISPLAY ROOMS\n' \
               '2.CREATE ROOM\n' \
               '3.JOIN ROOM\n' \
               '4.SWITCH ROOMS\n' \
               '5.DISPLAY USERS\n' \
               '6.DIRECT MESSAGE\n' \
               '7.LEAVE ROOM\n' \
               '8.DISPLAY MENU\n' \
               '9.QUIT\n' \
               '\nEnter Your Choice:'

#Class defination
class User:
    def __init__(self, name):
        self.name = name
        self.Room_object_dict = []
        self.thisRoom = ''

def Client_Send_Recv_Fun(client):
    nick=''
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            args = message.split(" ")
            name = Clients_socket_dict[args[0]]
            nick = args[0]
            if 'MSG_HELP' in message:
                name.send(instructions.encode('utf-8'))
            else:
                name.send('functionality yet to be added'.encode('utf-8'))

        except Exception as e:
            print("exception occured: ", e)
            index = Clients_list.index(client)
            Clients_list.remove(client)
            client.close()
          
            print(f'nick name is {nick}')
            if nick in Nick_names_list:
                Remove_Client_Fun(nick)
            if nick in Nick_names_list:
                Nick_names_list.remove(nick)
            #Message_broadcast(f'{nickname} left the room'.encode('utf-8'))
            break
# Processing received client messages
def receive_client_message():
    while True:
        client, address = server_socket.accept()
        print('Got connection from', address)
        #print(f'connected with {str(address)}')
        #print(client)
        client.send('MSG_PROVIDE_NAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        Nick_names_list.append(nickname)     #clients nickname list
        Clients_list.append(client)          #clients socket list

        #Create user object, and insert user objects/socket in dictonary
        user_obj = User(nickname)
        Users_object_dict[nickname] = user_obj   #This is dictionary which stores nickname to user object mapping
        Clients_socket_dict[nickname] = client   #this dictionary mapping between nickname and client_socket
        print(f'Nickname of the client is {nickname}')
        #client.send('Connected to the server!'.encode('utf-8'))
        client.send(instructions.encode('utf-8'))

        #Start seperate thread to communicate with each client
        thread = threading.Thread(target=Client_Send_Recv_Fun, args=(client,))
        thread.start()

# Creating a server socket instance and binding it with the declared port number
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_ip_address, server_port))
server_socket.listen()
print('Welcome to Internet Relay Chat')
print('Socket Successfully Created')
print('Server is in listen mode')
receive_client_message()



