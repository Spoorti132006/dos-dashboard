import socket
import threading

def attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9999))  # Replace with your server IP and port
        s.send(b"Hello Server")
        s.close()
    except:
        pass

for _ in range(50):  # Adjust number of threads to control intensity
    thread = threading.Thread(target=attack)
    thread.start()