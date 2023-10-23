import socket
from  threading import Thread

from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import autopy

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
# Create screen_height variable
screen_height = None

mouse = Controller()

# Define get_device_size() function
def get_device_size():
    # Access screen_height as global
    global screen_height
    # Loop through each monitor in the monitors returned by get_monitor()
    for monitor in get_monitors():
        # Calculate screen_height by :
                  #1. Convert monitor into string
                  #2. Split the string by , in a list
                  #3. Select 3 index of the list
                  #4. Use strip to remove spaces
                  #5. split using 'height=' string and select index 1
        screen_height = int(str(monitor).split(",")[3].strip().split('height=')[1])

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
                    # Calculate ypos as screen_height * (1 - (new_message["data"][1] - 0.2) / 0.6 )
                    ypos = screen_height * (1 - (new_message["data"][1] - 0.2) / 0.6 )
                    # using position(x,y) method on mouse object to move the cursor
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

    # Get the size of the screen
    get_device_size()
    accept_connections()

setup()
