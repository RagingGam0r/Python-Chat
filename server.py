import socket,select
import datetime


import time

print("I SERVER")

port = 12345

socket_list = []

users = {}
usersview = []
msgs = []
ipadress=input("Whats the servers ip address? ")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ipadress,port))

server_socket.listen(5)

socket_list.append(server_socket)

while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)

    #time.sleep(1)

    for sock in ready_to_read:

        if sock == server_socket:

            connect, addr = server_socket.accept()

            socket_list.append(connect)

            print("dude connected")

            connect.send(("You are connected from:" + str(addr)).encode('utf-8'))

        else:

            try:
            #if True == True:

                data = sock.recv(2048)


                data = data.decode('utf-8')


                data = data.split("\\/")

                if data[0].startswith("#"):


                    users[data[0][1:].lower()] = connect
                    datajoined = "User " + str(data[0][1:]) + " added."
                    print(datajoined)
                    for view in usersview:
                        view.send(datajoined.encode('utf-8'))

                    #connect.send(("Your user detail saved as : "+str(data[1:])).encode('utf-8'))

                elif data[0].startswith("/"):
                    data2 = data[0].split("/")
                    print(data2)
                    if data2[1] == "help":
                        data[1].send("help: Help command, connected: see whos connected")
                    elif data2[1] == "connected":
                        for view in usersview:
                            sendingdata = data[1][1:] + " Has request for active player list please wait"
                            view.send(sendingdata.encode('utf-8'))
                        active = ""
                        for view in usersview:
                            for user in users:
                                #view.send(user.encode('utf-8'))
                                active = active + user + " "
                        for view in usersview:
                            sendingdata = "The current active users are: " + str(active)
                            view.send(sendingdata.encode('utf-8'))
                elif data[0] == "exit":
                    for view in usersview:
                        view.send("Somebody has left! (notification only occurs if user quits properly)".encode('utf-8'))
                elif data[0] == "CLIENTVIEWPINGME":
                    usersview.append(connect)
                    for msg in msgs:
                        print("sending; ", msg)
                        connect.send(msg.encode('utf-8'))
                else:
                    currentDT = datetime.datetime.now()
                    msg = str(data[1][1:]) + " " + str(currentDT.strftime("%Y/%m/%d %H:%M:%S")) + " " + " > " + " " + str(data[0])
                    msg = str(msg)
                    msgs.append(msg)
                    print("Msg:", msg)
                    #users[data[1][1:]].send("Recieved".encode('utf-8'))
                    for view in usersview:
                        view.send(msg.encode('utf-8'))
                    #users[data[1:data.index(':')].lower()].send(data[data.index(':')+1:])

            except Exception as err:

                #print("Error:" , err)

                continue
    #time.sleep(1)
    """
    for i in users:
        print(i)
        print("Values:", users)
        print(users[i])
        users[i].send("TEST".encode('utf-8'))
    for i in usersview:
        print(i)
        i.send("TEST".encode('utf-8'))
    """

server_socket.close()