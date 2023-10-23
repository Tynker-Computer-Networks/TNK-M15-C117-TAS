import socket
from  threading import Thread

from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import autopy

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()

# TA2: Create mouse object using Controller class
mouse = Controller()

# TA2: Receive the message from the client
def recv_message(client_socket):
    # Access mouse as global
    global mouse

    # Create infinite while loop
    while True:
        # Start try block
        try:
            # Receive message from client_socket
            message = client_socket.recv(2048).decode()

            # TA2: Check if message exits
            if(message):
                # Eval the message string toi get a dictionary
                new_message  = eval(message)
                # Check if data key value is 'left_click'
                if(new_message["data"] == 'left_click'):
                    # Press left button using mouse object
                    mouse.press(Button.left)
                    # Release the  left button 
                    mouse.release(Button.left)
        # Add except block       
        except:
            # Pass
            pass


def accept_connections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")

        # TA2: Create a thread to receive the message from client
        thread_recv = Thread(target = recv_message, args=(client_socket,))
        thread_recv.start()


def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...\n")

    accept_connections()

setup()
