import socket, time, sys

count = int(sys.argv[1])
delay = float(sys.argv[2])

def send_burst(server_ip='127.0.0.1', port=9999, message="Hello Server"):
    for i in range(count):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, port))
            client.sendall(f"{message} #{i+1}".encode())
            response = client.recv(1024)
            print("Server replied:", response.decode())
            client.close()
        except Exception as e:
            print("Error:", e)
        time.sleep(delay)

send_burst()