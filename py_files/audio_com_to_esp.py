import socket
import os

#import esp8266_IP_scanner

#local_network = "192.168.137.0/24"
#ip_address = esp8266_IP_scanner.scan_network(local_network)

# ESP8266 server IP and port
#print(ip_address)

ESP8266_IP = "192.168.137.100"  # Replace with the actual IP address of your ESP8266
ESP8266_PORT = 8080

# File to send
FILE_PATH = 'C:/Users/SERGPC1/Desktop/Nexoai/py_files/output.wav'  # Replace with the path to your audio file

def send_file(file_path, esp_ip, esp_port):

           # Extract file name and validate extension
        filename = os.path.basename(file_path)
        valid_extensions = ['.mp3', '.wav', '.ogg', '.txt']
        if not any(filename.endswith(ext) for ext in valid_extensions):
            print("Error: File is not a supported audio type!")
            return

        # Open the file for reading in binary mode
        try:
            with open(file_path, 'rb') as file:
                # Create a socket connection
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((esp_ip, esp_port))
                    print(f"Connected to ESP8266 at {esp_ip}:{esp_port}")

                    # Send the file name
                    client_socket.sendall(f"{filename}\n".encode())
                    print(f"Sent file name: {filename}")

                    # Send the file data in chunks
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        client_socket.sendall(data)
                    print("Audio file sent successfully!")

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found!")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
  #  print(ip_address)
    send_file(FILE_PATH, ESP8266_IP, ESP8266_PORT)
