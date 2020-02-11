import socket

print("I CLIENT")

client_socket = socket.socket()

port = 12345

ipadress=input("Whats the servers ip address? ")

client_socket.connect((ipadress,port))

recv_msg = client_socket.recv(1023)

print(recv_msg)


name = ""
while not name.startswith("#"):
    name = input("Enter your user name: ")
    name = "#" + str(name)

datasending = name
client_socket.send(datasending.encode('utf-8'))



print("Joining")
print("JOINED PLEASE OPEN ClientView.py")


while True:

    send_msg = input("MSG: ")
    datasending = send_msg + "\\/" + name
    if send_msg == 'exit':
        client_socket.send(datasending.encode('utf-8'))
        break;
    else:
        client_socket.send(datasending.encode('utf-8'))

client_socket.close()