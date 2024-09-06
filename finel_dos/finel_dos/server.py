import socket
import threading
import time
import os
import datetime

# Global variables for tracking traffic and blacklisting IPs
ip_request_count = {}
blocked_ips = set()
request_threshold = 500  # Max requests per time period
time_window = 10  # Time window in seconds to measure traffic
blacklist_duration = 60  # Block IPs for this long in seconds

# Log file path
log_file_path = 'log.txt'

# Risk levels
low_risk_threshold = 100
high_risk_threshold = 300

# Blocking function
def block_ip(ip):
    blocked_ips.add(ip)
    print(f"Blocked IP: {ip}")
    threading.Timer(blacklist_duration, unblock_ip, [ip]).start()

# Unblocking function to remove IP from blocked list after a set time
def unblock_ip(ip):
    blocked_ips.remove(ip)
    print(f"Unblocked IP: {ip}")

# Reset request count after every time window
def reset_request_count():
    global ip_request_count
    while True:
        time.sleep(time_window)
        ip_request_count = {}

# Function to log detailed requests with risk levels
def log_request(ip, headers):
    # Determine risk level
    request_count = ip_request_count.get(ip, 0)
    risk_level = 'Low'
    if request_count > high_risk_threshold:
        risk_level = 'High'
    elif request_count > low_risk_threshold:
        risk_level = 'Medium'

    # Get the current time
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(log_file_path, 'a') as log_file:
        log_entry = f"Timestamp: {timestamp}\nRisk Level: {risk_level}\nIP: {ip}\n{headers}\n\n"
        log_file.write(log_entry)
        print(f"Logged: {log_entry.strip()}")

# Function to handle requests and detect potential DDoS
def handle_connection(client_socket, client_address):
    ip = client_address[0]
    
    if ip in blocked_ips:
        client_socket.close()
        return
    
    if ip in ip_request_count:
        ip_request_count[ip] += 1
    else:
        ip_request_count[ip] = 1
    
    # Check if the IP exceeds the threshold and block if necessary
    if ip_request_count[ip] > request_threshold:
        block_ip(ip)
        client_socket.close()
        return
    
    # Simulate legitimate traffic handling (responding to valid requests)
    try:
        request_data = client_socket.recv(4096).decode()
        headers = request_data.split('\r\n')
        log_request(ip, '\n'.join(headers))  # Log the request details

        # Serve index.html for GET requests
        if request_data.startswith('GET / HTTP/1.1'):
            with open('index.html', 'r') as file:
                response_body = file.read()
            response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response_body}"
        else:
            response = "HTTP/1.1 404 Not Found\n\nFile Not Found"
        
        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling request from {ip}: {e}")
    
    client_socket.close()

# Function to start the server and listen for connections
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    # Start thread to reset IP request counts every time window
    threading.Thread(target=reset_request_count, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_connection, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server("0.0.0.0", 7111)  # Make sure to run this on a separate port
