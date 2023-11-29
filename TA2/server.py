import socket
from  threading import Thread

from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import autopy

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
# Create screen_width variable

screen_height = None

mouse = Controller()

def get_device_size():
    # Access screen_width as global
    global screen_height, screen_width
    
    for monitor in get_monitors():
        #Get the width of a screen and store that value in the variable screen_width using monitor info.

        screen_height = monitor.height

def recv_message(client_socket):
    global mouse

    while True:
        try:
            message = client_socket.recv(2048).decode()

            if(message):
                new_message  = eval(message)
                if(new_message["data"] == 'left_click'):
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                elif(new_message["data"] == 'right_click'):
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                else:
                    # Calculate xpos as new_message["data"][0] * screen_width

                    ypos = screen_height * (1 - (new_message["data"][1] - 0.2) / 0.6 )
                    # Use xpos to position the mouse
                    mouse.position = (10, int(ypos))
                    
        except Exception as error:
            pass


def accept_connections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")
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

    get_device_size()
    accept_connections()

setup()
