import socket
import ipaddress
import threading

# To store the last active IP
last_active_ip = None
lock = threading.Lock()

# Function to scan a single IP
def scan_ip(ip):
    global last_active_ip
    try:
        # Attempt to connect to the IP on a common open port (e.g., port 8080)
        socket.create_connection((str(ip), 8080), timeout=0.5)
        print(f"[+] Active IP: {ip}")
        # Update the last active IP in a thread-safe manner
        with lock:
            last_active_ip = str(ip)
            
    except socket.error:
        pass

# Function to scan a range of IPs in a network
def scan_network(network):
    print(f"Scanning network: {network}")
    threads = []
    for ip in ipaddress.IPv4Network(network, strict=False):
        thread = threading.Thread(target=scan_ip, args=(ip,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    return last_active_ip

if __name__ == "__main__":
    # Define your local subnet (e.g., 192.168.137.0/24 for a 255.255.255.0 subnet)
    local_network = "192.168.137.0/24"
    scan_network(local_network)

    # Print the last active IP
    if last_active_ip:
        print(f"Last active IP: {last_active_ip}")
    else:
        print("No active IPs found.")
