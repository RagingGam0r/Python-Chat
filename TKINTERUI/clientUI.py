import socket
import tkinter as TK
from threading import *
import sys
import pickle

HEADER_LENGTH = 10

IP = str(input(" IP   : "))
PORT = str(input("PORT: "))

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))


username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

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

        self.inputbox = TK.Entry(self.window, width=50)
        self.inputbox.insert(0, "")
        self.inputbox.grid(row=2, column=1, padx=10, pady=10)

        self.sendinput = TK.Button(self.window, text="Send", width=20, command=self.sendmsg)
        self.sendinput.grid(row=3, column=1, padx=10, pady=10)

        self.txtMessages.config(state="normal")
        self.txtMessages.config(state="disabled")

        self.connecteduserslist.config(state="normal")
        self.connecteduserslist.config(state="disabled")

        test = RecvProtocool()
        test.start()


    def updateuser(self, userlist):
        self.connecteduserslist.config(state="normal")
        self.connecteduserslist.delete('1.0', TK.END)
        for i in userlist:
            self.connecteduserslist.insert(TK.END, (str(i) + "\n"))
        self.connecteduserslist.config(state="disabled")
        pass

    def addmsg(self, user, msg):
        #print("Adding: ", user, msg)
        self.txtMessages.config(state="normal")
        self.txtMessages.insert(TK.END, (str(user) + " > " + str(msg) + "\n"))
        self.txtMessages.config(state="disabled")

    def sendmsg(self):
        self.msg = self.inputbox.get()
        if self.msg:
            self.addmsg(username.decode("utf-8"), self.msg)
            self.msg = self.msg.encode("utf-8")
            message_header = f"{len(self.msg):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + self.msg)



    """
    def commands(self):
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
    """

class RecvProtocool(Thread):

    def __init__(self):
        super(RecvProtocool, self).__init__()
        self.msg = ""
        #self.start()

    def run(self):
        while True:
            #self.msg = client_socket.recv(HEADER_LENGTH)
            #print("Msg Recv: ", self.msg)
            username_header = client_socket.recv(HEADER_LENGTH)
            #print(username_header)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()

            try:
                username_length = int(username_header.decode("utf-8").strip())
                #print(username_length)
                username = client_socket.recv(username_length).decode("utf-8")
                #print(username)

                message_header = client_socket.recv(HEADER_LENGTH)
                #print(message_header)
                message_length = int(message_header.decode("utf-8").strip())
                #print(message_length)
                message = client_socket.recv(message_length)
                #print(message)


                try:
                    messagefinal = message.decode("utf-8")
                    app.addmsg(username, messagefinal)
                except Exception as err1:
                    try:
                        d = pickle.loads(message)
                        app.updateuser(d)
                    except Exception as err2:
                        raise Exception(
                            err1,
                            err2
                        )

            except Exception as err:
                print(err)
                raise err

def on_closing():
    pass



if __name__ == '__main__':
    root = TK.Tk()
    root.title('Client Log')
    root.geometry('{}x{}'.format(650, 550))
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.resizable(width = False, height = False)
    app = Ap(root)
    app.mainloop()


"""
while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

    try:
        while True:
            #receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            print(username_header)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode("utf-8").strip())
            print("us: ", username_length)
            username = client_socket.recv(username_length).decode("utf-8")
            print("us: ", username)

            message_header = client_socket.recv(HEADER_LENGTH)
            print("mh: ", message_header)
            message_length = int(message_header.decode("utf-8").strip())
            print("ml: ", message_length)
            message = client_socket.recv(message_length).decode("utf-8")
            print("mm: ", message)

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error", str(e))
        sys.exit()
"""
