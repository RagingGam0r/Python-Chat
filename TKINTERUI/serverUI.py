import tkinter as TK
import socket
import select
from threading import *
import pickle


HEADER_LENGTH = 10
IP = str(input(" IP   : "))
PORT = str(input("PORT: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

LARGE_FONT = ("Verdana", 12)

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}


    except:
        return False

def convert_to_header(message):
    message = str(message)
    return bytes(f"{len(message):<{HEADER_LENGTH}}", "utf-8")

class ServerC(Thread):

    def __init__(self):
        super(ServerC, self).__init__()
        self.sockets_list = [server_socket]

        self.clients = {}
        self.clientsnames = []

        self.start()



    def run(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()

                    user = receive_message(client_socket)
                    if user is False:
                        continue

                    self.sockets_list.append(client_socket)

                    self.clients[client_socket] = user

                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
                    app.addmsg("Server", f"Accepted new connection from: {user['data'].decode('utf-8')}")
                    self.clientsnames.append(user['data'].decode('utf-8'))
                    app.updateuser(self.clientsnames)

                    for csocket in self.clients:
                        #if csocket != client_socket:
                        message2 = f"Accepted new connection from: {user['data'].decode('utf-8')}"
                        csocket.send(convert_to_header("Server") + bytes(str("Server"), "utf-8") + convert_to_header(message2) + bytes(str(message2), "utf-8"))
                        message3 = pickle.dumps(self.clientsnames)
                        csocket.send(convert_to_header("Server") + bytes(str("Server"), "utf-8") + convert_to_header(message3) + message3)


                            # csocket.send(user['header'] + user['data'] + convert_to_header(message2) + bytes(str(message2), "utf-8"))

                else:
                    message = receive_message(notified_socket)
                    user = self.clients[notified_socket]
                    if message is False:
                        print("Closed existing connection from {}".format(self.clients[notified_socket]['data'].decode('utf-8')))
                        app.addmsg("Server", f"Closed existing connection from: {self.clients[notified_socket]['data'].decode('utf-8')}")
                        for client_socket in self.clients:
                            if client_socket != notified_socket:
                                message2 = "Closed existing connection from: {}".format(self.clients[notified_socket]['data'].decode('utf-8'))
                                client_socket.send(convert_to_header("Server") + bytes(str("Server"), "utf-8") + convert_to_header(message2) + bytes(str(message2), "utf-8"))
                        self.sockets_list.remove(notified_socket)
                        self.clientsnames.remove(self.clients[notified_socket]['data'].decode('utf-8'))
                        del self.clients[notified_socket]
                        app.updateuser(self.clientsnames)
                        for client_socket in self.clients:
                            if client_socket != notified_socket:
                                message3 = pickle.dumps(self.clientsnames)
                                print("sending pickle", message3)
                                client_socket.send(convert_to_header("Server") + bytes(str("Server"), "utf-8") + convert_to_header(message3) + message3)
                        continue

                    print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                    app.addmsg(user['data'].decode('utf-8'), message['data'].decode('utf-8'))

                    for client_socket in self.clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                self.clientsnames.remove(self.clients[notified_socket]['data'].decode('utf-8'))
                del self.clients[notified_socket]

server = ServerC()

class Ap(TK.Frame):

    def __init__(self, master):
        super().__init__(master) # initialize the 'TK.Frame'

        self.window = master

        self.conectedusersmsg = TK.Label(self.window, text='Connected users')
        self.conectedusersmsg.grid(column=2, row=0)

        self.connecteduserslist = TK.Text(self.window, width=25)
        self.connecteduserslist.grid(row=1, column=2, padx=10, pady=10)

        self.activechatmsg = TK.Label(self.window, text='Active Chat')
        self.activechatmsg.grid(column=1, row=0)

        self.txtMessages = TK.Text(self.window, width=50)
        self.txtMessages.grid(row=1, column=1, padx=10, pady=10)

        self.admincommand = TK.Entry(self.window, width=50)
        self.admincommand.insert(0, "")
        self.admincommand.grid(row=2, column=1, padx=10, pady=10)

        self.sendadmininput = TK.Button(self.window, text="Send", width=20, command=self.sendmsg)
        self.sendadmininput.grid(row=3, column=1, padx=10, pady=10)

        #self.updateuser(['server','RagingGam0r','Wistful'])
        #self.addmsg("RagingGam0r", "a")
        #self.addmsg("Wistful", "b")

        self.txtMessages.config(state="normal")
        self.txtMessages.config(state="disabled")

        self.connecteduserslist.config(state="normal")
        self.connecteduserslist.config(state="disabled")


    def updateuser(self, userlist):
        try:
            self.connecteduserslist.config(state="normal")
            self.connecteduserslist.delete('1.0', TK.END)
            for i in userlist:
                self.connecteduserslist.insert(TK.END, (str(i) + "\n"))
            self.connecteduserslist.config(state="disabled")
            pass
        except Exception as err:
            print(err)

    def addmsg(self, user, msg):
        try:
            print(user, msg)
            self.txtMessages.config(state="normal")
            self.txtMessages.insert(TK.END, (str(user) + " > " + str(msg) + "\n"))
            self.txtMessages.config(state="disabled")
        except Exception as err:
            print(err)

    def sendmsg(self):
        self.msg = self.admincommand.get()
        for client_socket in server.clients:
            if client_socket != server_socket:
                client_socket.send(convert_to_header("Server") + bytes(str("Server"), "utf-8") + convert_to_header(self.msg) + bytes(str(self.msg), "utf-8"))
                self.addmsg("Server", self.msg)
    """
    def commands(self):
        try:
            self.command = self.admincommand.get()
            print(self.command)
            if self.command.lower() == "/help":
                self.txtMessages.config(state="normal")
                self.addmsg("Server", "**--**HELP**--**")
                self.addmsg("Server", "/help > this")
                self.addmsg("Server", "/clearchat > clears chat")
                self.addmsg("Server", "/kickall > kick all users")
                self.addmsg("Server", "<Anything> > if does not have a / before it will be sent in format: Server > {MSG}")
                self.addmsg("Server", "Note: only you can see this")
                self.addmsg("Server", "**--**HELP**--**")
                self.txtMessages.config(state="disabled")
            elif self.command.lower() == "/clearchat":
                self.txtMessages.config(state="normal")
                self.txtMessages.delete('1.0', TK.END)
                self.txtMessages.config(state="disabled")

        except Exception as err:
            print(err)
    """


if __name__ == '__main__':
    root = TK.Tk()
    root.title('Server Log')
    root.geometry('{}x{}'.format(650, 550))
    root.resizable(width = False, height = False)
    app = Ap(root)
    app.mainloop()




































"""
class e(Thread):
    def __init__(self):
        super(e, self).__init__()
        self.i = 0
        self.start()
        
    def run(self):
        while True:
            self.i = self.i + 1
            listbox_log.insert(END, f"Cool, {self.i}")

            listbox_log.select_clear(listbox_log.size() - 2)
            listbox_log.yview(END)
            time.sleep(.1)

root = Tk()
frame = tk.Frame()
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.pack(expand=True, fill="both")

listbox_log = Listbox(frame)
scrollbar_log = Scrollbar(frame)

scrollbar_log.pack(side=RIGHT, fill="both")
listbox_log.pack(side=LEFT, fill="both")

listbox_log.configure(yscrollcommand=scrollbar_log.set)
scrollbar_log.configure(command=listbox_log.yview)
ee = e()
root.mainloop()

#while True:
#    print("test  print loop")
 #   time.sleep(.5)

"""
