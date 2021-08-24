import keyboard, functools
import socket, threading, time, sys


#encode and send keyboard events
def onEvent(s, event):
    msg = event.event_type + "\a" + event.name +"\r"
    msg = msg.encode("utf-8")
    s.sendall(msg)



print("Welcome to LaptopKeyboard, Made by Adam Cramer\n")

port = 25565
alive = True


#connect to remote server to send keypresses
def send():
    global alive
    #establish connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print("Trying to connect on " + str(otherIP) + ":" + str(port) + "...")
            s.connect((otherIP, port))
        except (socket.timeout, socket.gaierror, TimeoutError):
            print("\nUnable to connect to that IP address.")
            alive = False
            sys.exit(0)
        time.sleep(.2)
        print("Connection Successful")

        #capture keyboard inputs and send them to onEvent with a copy of the socket
        keyboard.hook(functools.partial(onEvent, s), True)
        keyboard.wait()



#dummy thread to keep our send tread alive
def dummy():
    while alive:
        time.sleep(.2)

#setup our threads
dThread = threading.Thread(target=dummy) #dummy thread
sThread = threading.Thread(target=send, daemon = True) #send thread

#start our thread
dThread.start()

otherIP = input("Please enter the target IPv4 address")

sThread.start()