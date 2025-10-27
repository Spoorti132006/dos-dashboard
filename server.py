import socket
import time
from collections import defaultdict

connection_log = defaultdict(list)
ALERT_THRESHOLD = 5
TIME_WINDOW = 10

def log_alert(ip, count):
    with open("alerts.txt", "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ALERT: High connection rate from {ip} ({count} in {TIME_WINDOW}s)\n")

def start_server(host='127.0.0.1', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        ip = addr[0]
        now = time.time()

        connection_log[ip].append(now)
        connection_log[ip] = [t for t in connection_log[ip] if now - t <= TIME_WINDOW]

        if len(connection_log[ip]) > ALERT_THRESHOLD:
            print(f"🚨 ALERT: High connection rate from {ip} ({len(connection_log[ip])} in {TIME_WINDOW}s)")
            log_alert(ip, len(connection_log[ip]))

        data = conn.recv(1024)
        if data:
            print(f"Received from {ip}: {data.decode()}")
            conn.sendall(b"ACK")
        conn.close()

start_server()