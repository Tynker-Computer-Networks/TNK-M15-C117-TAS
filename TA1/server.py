import socket
from  threading import Thread

# Import Required libraries and install 'pydroid 3' app on mobile to run main.py which is given as boiler 
# Button and Controller from pynput.mouse
from pynput.mouse import Button, Controller
# get_monitors from screeninfo
from screeninfo import get_monitors
# autopy library
import autopy

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()

def accept_connections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")

def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...\n")


setup()
