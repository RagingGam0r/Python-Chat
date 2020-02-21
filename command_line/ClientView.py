import socket

print("I CLIENT VIEW")

client_socket = socket.socket()

port = 12345

ipadress=input("Whats the servers ip address? ")

client_socket.connect((ipadress,port))



recv_msg = client_socket.recv(1024)

print(recv_msg)

print("/!\\ WARNING If this ui suddenly closes it could be; invalid ip, lost connection, server is offline/crashes WARNING /!\\")


client_socket.send("CLIENTVIEWPINGME".encode('utf-8'))



print("Joining")

while True:

    recv_msg = client_socket.recv(1024)

    print (recv_msg.decode('utf-8'))


client_socket.close()
